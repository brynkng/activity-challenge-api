import os
import traceback

import requests
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from api.custom_errors import ApiAuthError, ApiError
from api.models import Profile, CompetitionInvitation


def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]

    return helper


def store_fitbit_auth(code, server_host, profile):
    client_id = os.environ['FITBIT_CLIENT_ID']

    data = {
        'client_id': client_id,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f"http://{server_host}/api/store_fitbit_auth",
        'expires_in': 2592000
    }

    return _send_auth_request(profile, data)


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


def _build_data(profile):
    return {'competitions': [_build_competition_summary(profile, competition) for competition in
                             profile.competitions.all()]}


def _build_competition_summary(profile, competition):
    friend_list = get_competition_friend_list(profile, competition)
    profile_ids = [f['profile_id'] for f in friend_list]
    profiles = Profile.objects.filter(id__in=profile_ids)

    def _get_profile(id):
        return [p for p in profiles if p.id == id][0]

    competition_members = [
        _add_point_details(competition, f, profile)
        for f in friend_list if f['in_competition']
    ]
    # competition_members = [
    #     _add_point_details(competition, f, _get_profile(f['profile_id']))
    #     for f in friend_list if f['in_competition']
    # ]

    invitable_friends = [f for f in friend_list if f['in_app'] and not f['in_competition']]

    competition_info = {
        'id': competition.id,
        'name': competition.name,
        'point_details': _add_point_details(competition, {}, profile),
        'competition_members': competition_members,
        'invitable_friends': invitable_friends

    }

    return competition_info


def _add_point_details(competition, init_data, profile):
    point_system = competition.point_system

    # activity_response = requests.get(f"https://api.fitbit.com/1/user/{profile.fitbit_user_id}/activities/date/today.json",
    #                                  headers=get_auth_headers(profile.access_token))
    activity_response = requests.get(f"https://api.fitbit.com/1/user/-/activities/date/today.json",
                                     headers=get_auth_headers(profile.access_token))
    _validate_response(activity_response)

    activity_response = activity_response.json()
    if 'summary' in activity_response and 'heartRateZones' in activity_response['summary']:
        summary = activity_response['summary']

        active_minutes = summary['fairlyActiveMinutes'] + summary['veryActiveMinutes']

        cardio_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Cardio'][0]
        peak_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Peak'][0]

        points = (point_system.active_minute_points * active_minutes) + \
                 (point_system.cardio_zone_points * cardio_zone_minutes) + \
                 (point_system.peak_zone_points * peak_zone_minutes)

        init_data['points'] = points
        init_data['active_minutes'] = active_minutes
        init_data['active_minute_factor'] = point_system.active_minute_points
        init_data['cardio_zone_minutes'] = cardio_zone_minutes
        init_data['cardio_zone_factor'] = point_system.cardio_zone_points
        init_data['peak_zone_minutes'] = peak_zone_minutes
        init_data['peak_zone_factor'] = point_system.peak_zone_points

    return init_data


def retrieve_fitbit_data(profile, server_host):
    token_expiration = profile.token_expiration
    access_token = profile.access_token
    authorized = bool(access_token)
    expired = token_expiration and token_expiration < timezone.now()
    data = {'authorized': authorized}

    try:
        if expired:
            authorized = _refresh_token(profile)

        if authorized:
            data['data'] = _build_data(profile)
        else:
            data['auth_url'] = _auth_url(server_host)
    except ApiAuthError:
        traceback.print_exc()
        data['errors'] = 'Fitbit auth error. Please re-authenticate.'
        data['auth_url'] = _auth_url(server_host)
        data['authorized'] = False

    return data


def _auth_url(server_host):
    client_id = os.environ['FITBIT_CLIENT_ID']
    return f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=" \
        f"http://{server_host}/api/store_fitbit_auth&scope=activity%20heartrate%20profile%20social"


def _refresh_token(profile):
    print("Refreshing token")
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': profile.refresh_token
    }

    return _send_auth_request(profile, data)


def _send_auth_request(profile, data):
    client_id = os.environ['FITBIT_CLIENT_ID']
    encoded_auth_key = urlsafe_base64_encode(str.encode(f"{client_id}:{os.environ['FITBIT_CLIENT_SECRET']}")).decode("utf-8")
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
