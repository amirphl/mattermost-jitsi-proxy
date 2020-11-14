import json
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from proxy.cache_repo import CacheRepository
from proxy.utils import decrypt, get_driver


class LoginView(APIView):
    MATTER_MOST_LOGIN_ENDPOINT = settings.MATTERMOST_API_ENDPOINT + '/api/v4/users/login'

    def post(self, *args, **kwargs):
        try:
            auth_token = self.request.META.get('HTTP_AUTH_TOKEN')
            if auth_token is None:
                auth_token = self.request.META['headers']['HTTP_AUTH_TOKEN']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'HTTP_AUTH_TOKEN header not found'})

        try:
            credentials = json.loads(decrypt(auth_token))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'received invalid token'})

        try:
            channel = credentials['channel']
            team = credentials['team']
            room_id = credentials['room_id']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'team, channel or room_id not provided'})

        try:
            driver = get_driver(credentials.get('login_id', None),
                                credentials.get('password', None))
            driver.login()
            data = {'access_token': driver.client.token,
                    'channel': channel,
                    'team': team}
            CacheRepository.store(room_id, str(data), 300000)  # todo fix it

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
