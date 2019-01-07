import os
import requests
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone


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

    return {'success': r.get('success', False), 'errors': str(r.get('errors', ''))}


def _build_data(profile, access_token):
    data = {'competitions': []}
    for competition in profile.competitions.all():

        # TODO do for each friend in competition
        competition_info = _build_competition_info(competition, access_token)

        data['competitions'].append(competition_info)
    # caching?
    # Display details of currently running

    # friends_response = requests.get('https://api.fitbit.com/1/user/-/friends.json', headers=headers).json()
    # active minutes, heart rate zones, friends
    return data


def _build_competition_info(competition, access_token):

    point_system = competition.point_system
    headers = {'Authorization': f"Bearer {access_token}"}
    # TODO return different time series data depending on competition type
    activity_response = requests.get('https://api.fitbit.com/1/user/-/activities/date/today.json', headers=headers).json()

    summary = activity_response['summary']
    active_minutes = summary['fairlyActiveMinutes'] + summary['veryActiveMinutes']
    cardio_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Cardio'][0]
    peak_zone_minutes = [i['minutes'] for i in summary['heartRateZones'] if i['name'] == 'Peak'][0]
    points = (point_system.active_minute_points * active_minutes) + \
             (point_system.cardio_zone_points * cardio_zone_minutes) + \
             (point_system.peak_zone_points * peak_zone_minutes)
    competition_info = {
        'name': competition.name,
        'points': points,
        'active_minutes': active_minutes,
        'cardio_zone_minutes': cardio_zone_minutes,
        'peak_zone_minutes': peak_zone_minutes
    }
    return competition_info


def retrieve_fitbit_data(profile, server_host):
    token_expiration = profile.token_expiration
    access_token = profile.access_token
    authorized = bool(access_token)
    expired = token_expiration and token_expiration < timezone.now()
    errors = None

    if expired:
        r = _refresh_token(profile)
        authorized = r.get('success')
        errors = r.get('errors', None)

    data = {'success': True, 'authorized': authorized}

    if authorized:
        try:
            data['data'] = _build_data(profile, access_token)

            if data['data'].get('errors', None):
                errors = data['data'].get('errors')
        except AttributeError as err:
            errors = str(err)
    else:
        data['auth_url'] = _auth_url(server_host)

    if errors:
        data['errors'] = errors
        data['auth_url'] = _auth_url(server_host)
        data['success'] = False

    return data


def _auth_url(server_host):
    client_id = os.environ['FITBIT_CLIENT_ID']
    return f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=" \
        f"http://{server_host}/api/store_fitbit_auth&scope=activity%20heartrate%20profile%20social"


def _refresh_token(profile):
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

    r = {'success': bool(access_token)}
    if response.get('errors', None):
        r['errors'] = str(response.get('errors'))
        return r

    profile.access_token = access_token
    profile.refresh_token = refresh_token
    profile.token_expiration = timezone.now() + timezone.timedelta(seconds=response.get('expires_in'))
    profile.save()

    return r