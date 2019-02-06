import os

from api.custom_errors import ApiAuthError, ApiError
from django.utils.http import urlsafe_base64_encode
from django.utils import timezone
import requests


class FitbitApiGateway:
    def __init__(self, profile):
        self.__validate_api_access(profile)

    @staticmethod
    def auth_url(url_start):
        client_id = os.environ['FITBIT_CLIENT_ID']
        return f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri=" \
            f"{url_start}/api/store_fitbit_auth&scope=activity%20heartrate%20profile%20social"

    def send_auth_request(self, profile, data):
        client_id = os.environ['FITBIT_CLIENT_ID']
        encoded_auth_key = urlsafe_base64_encode(str.encode(f"{client_id}:{os.environ['FITBIT_CLIENT_SECRET']}")).decode(
            "utf-8")
        headers = {
            'Authorization': f"Basic {encoded_auth_key}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(
            'https://api.fitbit.com/oauth2/token', headers=headers, data=data)
        self.__validate_response(response)

        return response.json()

    def get_profile(self, profile):
        response = requests.get('https://api.fitbit.com/1/user/-/profile.json',
                                headers=self.__get_auth_headers(profile.access_token))
        self.__validate_response(response)

        return response.json()

    def get_friends(self, profile):
        response = requests.get('https://api.fitbit.com/1/user/-/friends.json',
                                headers=self.__get_auth_headers(profile.access_token))
        self.__validate_response(response)

        return response.json().get('friends', [])

    def get_heart_data(self, start, end, profile):
        url = f"https://api.fitbit.com/1/user/{profile.fitbit_user_id}/activities/heart/date/{start}/{end}.json"
        activity_response = requests.get(url, headers=self.__get_auth_headers(profile.access_token))
        self.__validate_response(activity_response)
        
        return activity_response.json().get('activities-heart')

    def get_activities_data(self, profile, start, end, key):
        url = f"https://api.fitbit.com/1/user/{profile.fitbit_user_id}/activities/tracker/{key}/date/{start}/{end}.json"
        activity_response = requests.get(url, headers=self.__get_auth_headers(profile.access_token))
        self.__validate_response(activity_response)
        
        return activity_response.json().get('activities-tracker-' + key)

    def __validate_response(self, response):
        json_response = response.json()
        errors = ', '.join([e['message'] for e in response.json()[
            'errors']]) if 'errors' in json_response else ''

        if response.status_code == 401:
            raise ApiAuthError(errors)
        elif response.status_code != 200:
            raise ApiError(errors)

    def __refresh_token(self, profile):
        print("Refreshing token")
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': profile.refresh_token
        }

        self.send_auth_request(profile, data)

    def __get_auth_headers(self, access_token):
        return {'Authorization': f"Bearer {access_token}"}

    def __validate_api_access(self, profile):
        token_expiration = profile.token_expiration
        access_token = profile.access_token

        if not access_token:
            raise ApiAuthError("No access token!")

        expired = token_expiration and token_expiration < timezone.now()

        if expired:
            self.__refresh_token(profile)
