from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class MockResponse:
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.json_data


class LoginAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.auth_token = 'some token'
        self.endpoint = '/api/v1/login/'
        self.http_auth_token_header = 'HTTP_AUTH_TOKEN'

    @mock.patch('proxy.views.decrypt')
    @mock.patch('requests.post')
    @mock.patch('proxy.cache_repo.CacheRepository.store')
    def test_successful(self, store, post, decrypt):
        decrypt.return_value = '{"login_id": "a username",' \
                               '"password": "a password",' \
                               '"team": "a team",' \
                               '"channel": "a channel",' \
                               '"room_id": "a room_id"}'
        post.return_value = MockResponse({}, 201, {'Token': 'some another token'})
        store.return_value = None
        res = self.client.post(self.endpoint, headers={self.http_auth_token_header: self.auth_token})
        decrypt.assert_called_once()
        post.assert_called_once()
        store.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(res.data)

    def test_no_token(self):
        res = self.client.post(self.endpoint)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {'message': 'HTTP_AUTH_TOKEN header not found'})

    @mock.patch('proxy.views.decrypt')
    def test_invalid_token_data(self, decrypt):
        decrypt.return_value = b'im not json'
        res = self.client.post(path=self.endpoint, headers={self.http_auth_token_header: self.auth_token})
        decrypt.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {'message': 'received invalid token'})

    # @mock.patch.object(json, 'loads')
    @mock.patch('proxy.views.decrypt')
    def test_no_team_channel(self, decrypt):
        decrypt.return_value = b'{}'
        res = self.client.post(path=self.endpoint, headers={self.http_auth_token_header: self.auth_token})
        decrypt.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {'message': 'team, channel or room_id not provided'})

    @mock.patch('proxy.views.decrypt')
    @mock.patch('requests.post')
    def test_no_username_password(self, post, decrypt):
        decrypt.return_value = '{"team": "a team",' \
                               '"channel": "a channel",' \
                               '"room_id": "a room_id"}'
        post.return_value = MockResponse({'message': 'unauthorized'}, 401)
        res = self.client.post(self.endpoint, headers={self.http_auth_token_header: self.auth_token})
        decrypt.assert_called_once()
        post.assert_called_once()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data, {'message': 'unauthorized'})
