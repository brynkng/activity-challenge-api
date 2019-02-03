from datetime import datetime, time
import os
import traceback
from functools import reduce

import pytz
import requests
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from api.custom_errors import ApiAuthError, ApiError
from api.models import Profile, CompetitionInvitation, CompetitionScore, Competition


def store_fitbit_auth(code, url_start, profile):
    client_id = os.environ['FITBIT_CLIENT_ID']

    data = {
        'client_id': client_id,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f"{url_start}/api/store_fitbit_auth",
        'expires_in': 2592000
    }

    _send_auth_request(profile, data)

    _save_display_name(profile)


def _save_display_name(profile):
    response = requests.get('https://api.fitbit.com/1/user/-/profile.json',
                            headers=get_auth_headers(profile.access_token))
    _validate_response(response)
    profile.display_name = response.json()['user']['displayName']
    profile.save()


def get_auth_headers(access_token):
    return {'Authorization': f"Bearer {access_token}"}


def get_competition_friend_list(profile, competition):
    friends_response = get_friends(profile)
    fitbit_ids = [f['user']['encodedId'] for f in friends_response]

    # TODO possibly clean this up just working with profile querysets? preload competitions and invitations?
    id_tuples = Profile.objects.filter(fitbit_user_id__in=fitbit_ids).values_list('id', 'fitbit_user_id')
    profile_to_fitbit = {ids[0]: ids[1] for ids in id_tuples}
    fitbit_to_profile = {ids[1]: ids[0] for ids in id_tuples}
    in_competition = Profile.competitions.through.objects.filter(
        competition_id=competition.id,
        profile_id__in=profile_to_fitbit.keys()
    ).values_list('profile_id', flat=True)

    def _build_friend_list(f):
        info = f['user']
        fitbit_id = info['encodedId']
        profile_id = fitbit_to_profile.get(fitbit_id, None)
        invited = CompetitionInvitation.objects.filter(profile=profile_id, competition=competition.id).exists()

        return {
            'display_name': info['displayName'],
            'avatar': info['avatar'],
            'in_app': fitbit_id in fitbit_to_profile,
            'in_competition': profile_id in in_competition,
            'invited': invited,
            'profile_id': profile_id,
            'fitbit_id': fitbit_id
        }

    return list(map(_build_friend_list, friends_response))


def get_friends(profile):
    response = requests.get('https://api.fitbit.com/1/user/-/friends.json',
                            headers=get_auth_headers(profile.access_token))
    _validate_response(response)

    return response.json().get('friends', [])


def _build_simple_competitions_data(profile):
    return {'competitions': [_build_simple_competition(profile, competition) for competition in
                             profile.competitions.all()]}


def _update_competition_scores(competition):
    scores = []

    for profile in competition.profile_set.all():
        score = profile.competition_scores.filter(competition_id=competition.id).last()

        competition_end = datetime(competition.end.year, competition.end.month, competition.end.day, 23, 59, 59,
                                   tzinfo=pytz.UTC)

        score_out_of_date = score and ((competition.has_ended() and score.updated_at < competition_end) or (
                not competition.has_ended() and score.updated_at + timezone.timedelta(minutes=10) < timezone.now()))

        if not score:
            data = _retrieve_point_details(competition, {}, profile)
            score = CompetitionScore.objects.create(
                point_total=data.get('points'),
                competition=competition,
                profile=profile
            )
            score.save()

        elif score_out_of_date:
            data = _retrieve_point_details(competition, {}, profile)
            score.point_total = data.get('points')
            score.save()

        scores.append(score)

    return scores


def _build_simple_competition(profile, competition):
    scores = _update_competition_scores(competition)
    score = [score for score in scores if profile.id == score.profile.id][0]

    return {
        'id': competition.id,
        'name': competition.name,
        'points': score.point_total,
        'current': not competition.has_ended(),
        'winner': _get_winner(competition, scores)
    }


def _get_winner(competition, scores=None):
    if competition.has_ended():
        if not scores:
            scores = _update_competition_scores(competition)

        scores.sort(key=lambda s: s.point_total)
        winner = scores[-1]

        return {'name': winner.profile.display_name, 'points': winner.point_total}
    else:
        return None


def _build_detailed_competition(profile, competition):
    friend_list = get_competition_friend_list(profile, competition)
    profile_ids = [f['profile_id'] for f in friend_list]
    profiles = Profile.objects.filter(id__in=profile_ids)

    def _get_profile(id): return [p for p in profiles if p.id == id][0]

    competition_members = [
        _retrieve_point_details(competition, f, _get_profile(f['profile_id']))
        for f in friend_list if f['in_competition']
    ]

    invitable_friends = [f for f in friend_list if f['in_app'] and not f['in_competition']]

    return {
        'id': competition.id,
        'name': competition.name,
        'point_details': _retrieve_point_details(competition, {}, profile),
        'current': not competition.has_ended(),
        'winner': _get_winner(competition),
        'competition_members': competition_members,
        'invitable_friends': invitable_friends

    }


def _retrieve_point_details(competition, init_data, profile):
    point_system = competition.point_system

    start = competition.start.strftime('%Y-%m-%d')
    end = competition.end.strftime('%Y-%m-%d')

    def retrieve_activity_data(key):
        url = f"https://api.fitbit.com/1/user/{profile.fitbit_user_id}/activities/tracker/{key}/date/{start}/{end}.json"
        activity_response = requests.get(url, headers=get_auth_headers(profile.access_token))
        _validate_response(activity_response)
        return activity_response.json().get(f"activities-tracker-{key}")

    init_data['fairly_active_data'] = retrieve_activity_data('minutesFairlyActive')
    init_data['very_active_data'] = retrieve_activity_data('minutesVeryActive')

    url = f"https://api.fitbit.com/1/user/{profile.fitbit_user_id}/activities/heart/date/{start}/{end}.json"
    activity_response = requests.get(url, headers=get_auth_headers(profile.access_token))
    _validate_response(activity_response)
    init_data['heart_rate_data'] = activity_response.json().get('activities-heart')

    def get_active_minutes(key): return reduce((lambda acc, r: int(r['value']) + acc), init_data[key], 0)

    def get_hr_minutes(key):
        return reduce(
            (lambda acc, r: int(
                [i.get('minutes', 0) for i in r['value']['heartRateZones'] if i['name'] == key][0]) + acc),
            init_data['heart_rate_data'], 0)

    active_minutes = get_active_minutes('fairly_active_data') + get_active_minutes('very_active_data')
    cardio_zone_minutes = get_hr_minutes('Cardio')
    peak_zone_minutes = get_hr_minutes('Peak')

    init_data['points'] = (point_system.active_minute_points * active_minutes) + \
                          (point_system.cardio_zone_points * cardio_zone_minutes) + \
                          (point_system.peak_zone_points * peak_zone_minutes)

    init_data['active_minutes'] = active_minutes
    init_data['cardio_zone_minutes'] = cardio_zone_minutes
    init_data['peak_zone_minutes'] = peak_zone_minutes
    init_data['active_minute_factor'] = point_system.active_minute_points
    init_data['cardio_zone_factor'] = point_system.cardio_zone_points
    init_data['peak_zone_factor'] = point_system.peak_zone_points

    print(init_data)

    return init_data


def get_detailed_competition(profile, url_start, competition_id):
    competition = Competition.objects.filter(id=competition_id).last()
    data = validate_fitbit_access(profile, url_start)

    if data.get('authorized'):
        data['data'] = _build_detailed_competition(profile, competition)

    return data


def get_simple_competitions_list(profile, url_start):
    data = validate_fitbit_access(profile, url_start)

    if data.get('authorized'):
        data['data'] = _build_simple_competitions_data(profile)

    return data


def validate_fitbit_access(profile, url_start):
    token_expiration = profile.token_expiration
    access_token = profile.access_token
    authorized = bool(access_token)
    expired = token_expiration and token_expiration < timezone.now()
    data = {'authorized': authorized}

    try:
        if expired:
            authorized = _refresh_token(profile)

        if not authorized:
            data['auth_url'] = _auth_url(url_start)

    except ApiAuthError:
        traceback.print_exc()
        data['errors'] = 'Fitbit auth error. Please re-authenticate.'
        data['auth_url'] = _auth_url(url_start)
        data['authorized'] = False

    return data


def _auth_url(url_start):
    client_id = os.environ['FITBIT_CLIENT_ID']
    return f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=" \
        f"{url_start}/api/store_fitbit_auth&scope=activity%20heartrate%20profile%20social"


def _refresh_token(profile):
    print("Refreshing token")
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': profile.refresh_token
    }

    return _send_auth_request(profile, data)


def _send_auth_request(profile, data):
    client_id = os.environ['FITBIT_CLIENT_ID']
    encoded_auth_key = urlsafe_base64_encode(str.encode(f"{client_id}:{os.environ['FITBIT_CLIENT_SECRET']}")).decode(
        "utf-8")
    headers = {
        'Authorization': f"Basic {encoded_auth_key}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data)
    _validate_response(response)

    json_response = response.json()
    profile.access_token = json_response['access_token']
    profile.refresh_token = json_response['refresh_token']
    profile.token_expiration = timezone.now() + timezone.timedelta(seconds=(json_response['expires_in']))
    profile.fitbit_user_id = json_response['user_id']
    profile.save()

    return True


def _validate_response(response):
    json_response = response.json()
    errors = ', '.join([e['message'] for e in response.json()['errors']]) if 'errors' in json_response else ''

    if response.status_code == 401:
        raise ApiAuthError(errors)
    elif response.status_code != 200:
        raise ApiError(errors)
