import os
from .fitbit_provider import FitbitProvider


class AuthProvider(FitbitProvider):

    def update_authorization(self, profile):
        response = self.gateway.send_auth_request(profile, data)

        profile.access_token = response['access_token']
        profile.refresh_token = response['refresh_token']
        profile.token_expiration = timezone.now(
        ) + timezone.timedelta(seconds=(response['expires_in']))
        profile.fitbit_user_id = response['user_id']
        profile.save()

        return True

    def store_fitbit_auth(self, code, url_start, profile):
        client_id = os.environ['FITBIT_CLIENT_ID']

        data = {
            'client_id': client_id,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': f"{url_start}/api/store_fitbit_auth",
            'expires_in': 2592000
        }

        self.update_authorization(profile, data)

        self.__save_display_name(profile)

    def __save_display_name(profile):
        response = self.gateway.get_profile()
        profile.display_name = response['user']['displayName']
        profile.save()
