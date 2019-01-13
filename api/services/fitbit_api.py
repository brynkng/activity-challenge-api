import os
import traceback

import requests
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
from api.custom_errors import AuthError
from api.models import Profile


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
    r = _send_auth_request(profile, data)

    return {'success': r.get('success', False)}


def get_auth_headers(access_token):
    return {'Authorization': f"Bearer {access_token}"}


def get_competition_friend_list(profile, competition):
    friends_response = get_friends(profile)
    fitbit_ids = [f['user']['encodedId'] for f in friends_response]

    id_tuples = Profile.objects.filter(fitbit_user_id__in=fitbit_ids).values_list('id', 'fitbit_user_id')
    profile_to_fitbit = {ids[0]: ids[1] for ids in id_tuples}
    fitbit_to_profile = {ids[1]: ids[0] for ids in id_tuples}
    in_competition = Profile.competitions.through.objects.filter(
        competition_id=competition.id,
        profile_id__in=profile_to_fitbit.keys()
    ).values_list('profile_id', flat=True)

    # TODO invited

    def _build_friend_list(f):
        info = f['user']
        fitbit_id = info['encodedId']
        profile_id = fitbit_to_profile.get(fitbit_id, None)

        return {
            'display_name': info['displayName'],
            'avatar': info['avatar'],
            'in_app': fitbit_id in fitbit_to_profile,
            'in_competition': profile_id in in_competition,
            'invited': False,
            'profile_id': profile_id,
            'fitbit_id': fitbit_id
        }

    return list(map(_build_friend_list, friends_response))


def get_friends(profile):
    response = requests.get('https://api.fitbit.com/1/user/-/friends.json',
                            headers=get_auth_headers(profile.access_token)).json()
    print('-' * 100)
    print(response)
    if 'errors' in response:
        raise AuthError(str(response['errors']))

    return response.get('friends', [])


def _build_data(profile):
    return {'competitions': [_build_competition_summary(profile, competition) for competition in
                             profile.competitions.all()]}


def _build_competition_summary(profile, competition):
    friend_list = get_competition_friend_list(profile, competition)

    profile_ids = [f['profile_id'] for f in friend_list]
    token_tuples = Profile.objects.filter(id__in=profile_ids).values_list('id', 'access_token')
    profile_to_token = {t[0]: t[1] for t in token_tuples}

    competition_members = [
        _add_point_details(competition, f, profile.access_token, f['fitbit_id'])
        for f in friend_list if f['in_competition']
    ]
    # competition_members = [
    #     _add_point_details(competition, f, profile_to_token[f['profile_id']], f['fitbit_id'])
    #     for f in friend_list if f['in_competition']
    # ]

    invitable_friends = [f for f in friend_list if f['in_app'] and not f['in_competition']]

    competition_info = {
        'id': competition.id,
        'name': competition.name,
        'point_details': _add_point_details(competition, {}, profile.access_token, profile.fitbit_user_id),
        'competition_members': competition_members,
        'invitable_friends': invitable_friends

    }

    return competition_info


def _add_point_details(competition, starting_data, access_token, fitbit_id):
    point_system = competition.point_system

    # activity_response = requests.get(f"https://api.fitbit.com/1/user/{fitbit_id}/activities/date/today.json",
    #                                  headers=get_auth_headers(access_token)).json()
    activity_response = requests.get(f"https://api.fitbit.com/1/user/-/activities/date/today.json",
                                     headers=get_auth_headers(access_token)).json()
    if 'errors' in activity_response:
        raise AuthError(activity_response['errors'])

    if 'summary' in activity_response and 'heartRateZones' in activity_response['summary']:
        summary = activity_response['summary']

        active_minutes = summary['fairlyActiveMinutes'] + summary['veryActiveMinutes']

        cardio_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Cardio'][0]
        peak_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Peak'][0]

        points = (point_system.active_minute_points * active_minutes) + \
                 (point_system.cardio_zone_points * cardio_zone_minutes) + \
                 (point_system.peak_zone_points * peak_zone_minutes)

        starting_data['points'] = points
        starting_data['active_minutes'] = active_minutes
        starting_data['cardio_zone_minutes'] = cardio_zone_minutes
        starting_data['peak_zone_minutes'] = peak_zone_minutes

    return starting_data


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
    except AuthError as error:
        traceback.print_exc()
        data['errors'] = str(error)
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
    encoded_auth_key = urlsafe_base64_encode(str.encode(f"{client_id}:{os.environ['FITBIT_CLIENT_SECRET']}")).decode(
        "utf-8")
    headers = {
        'Authorization': f"Basic {encoded_auth_key}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://api.fitbit.com/oauth2/token', headers=headers, data=data).json()

    access_token = response.get('access_token', None)
    refresh_token = response.get('refresh_token', None)
    fitbit_user_id = response.get('user_id', None)

    if 'errors' in response:
        raise AuthError(str(response['errors']))

    profile.access_token = access_token
    profile.refresh_token = refresh_token
    profile.token_expiration = timezone.now() + timezone.timedelta(seconds=response.get('expires_in'))
    profile.fitbit_user_id = fitbit_user_id
    profile.save()

    return True
