from datetime import datetime, time
import os
import traceback
from functools import reduce

import pytz
import requests
from django.utils import timezone
from api.custom_errors import ApiAuthError, ApiError
from api.models import Profile, CompetitionInvitation, CompetitionScore, Competition

def get_competition_friend_list(profile, competition):
    friends_response = get_friends(profile)
    fitbit_ids = [f['user']['encodedId'] for f in friends_response]

    # TODO possibly clean this up just working with profile querysets? preload competitions and invitations?
    id_tuples = Profile.objects.filter(
        fitbit_user_id__in=fitbit_ids).values_list('id', 'fitbit_user_id')
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
        invited = CompetitionInvitation.objects.filter(
            profile=profile_id, competition=competition.id).exists()

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


def _build_simple_competitions_data(profile):
    return {'competitions': [_build_simple_competition(profile, competition) for competition in
                             profile.competitions.all()]}


def _update_competition_scores(competition):
    scores = []

    for profile in competition.profile_set.all():
        score = profile.competition_scores.filter(
            competition_id=competition.id).last()

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
    data = _get_competition_data(competition, scores)
    data['points'] = score.point_total

    return data


def _get_winner(competition, scores=None):
    if competition.has_ended():
        if not scores:
            scores = _update_competition_scores(competition)

        scores.sort(key=lambda s: s.point_total)
        winner = scores[-1]

        return {'name': winner.profile.display_name, 'points': winner.point_total}
    else:
        return None


def _get_competition_data(competition, scores=None):
    return {
        'id': competition.id,
        'name': competition.name,
        'start': competition.start,
        'end': competition.end.strftime('%Y-%m-%d'),
        'current': not competition.has_ended(),
        'winner': _get_winner(competition, scores)
    }


def _build_detailed_competition(profile, competition):
    friend_list = get_competition_friend_list(profile, competition)
    profile_ids = [f['profile_id'] for f in friend_list]
    profiles = Profile.objects.filter(id__in=profile_ids)

    def _get_profile(id): return [p for p in profiles if p.id == id][0]

    competition_members = [
        _retrieve_point_details(competition, f, _get_profile(f['profile_id']))
        for f in friend_list if f['in_competition']
    ]

    invitable_friends = [
        f for f in friend_list if f['in_app'] and not f['in_competition']]

    data = _get_competition_data(competition)
    data['point_details'] = _retrieve_point_details(competition, {}, profile)
    data['competition_members'] = competition_members
    data['invitable_friends'] = invitable_friends

    return data


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

    def get_active_minutes(key): return reduce(
        (lambda acc, r: int(r['value']) + acc), init_data[key], 0)

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

    if data.get('authorized'):
        data['data'] = _build_detailed_competition(profile, competition)

    return data


def get_simple_competitions_list(profile, url_start):
    return _build_simple_competitions_data(profile)
