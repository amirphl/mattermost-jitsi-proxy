from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# class MockResponse:
#     def __init__(self, json_data, status_code, headers=None):
#         self.json_data = json_data
#         self.status_code = status_code
#         self.headers = headers
#
#     def json(self):
#         return self.json_data


# class LoginAPITests(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.auth_token = 'some token'
#         self.endpoint = '/api/v1/login/'
#         self.http_auth_token_header = 'HTTP_AUTH_TOKEN'
#
#     @mock.patch('proxy.views.decrypt')
#     @mock.patch('proxy.views.get_driver')
#     @mock.patch('proxy.cache_repo.CacheRepository.store')
#     def test_success(self, store, get_driver, decrypt):
#         decrypt.return_value = '{"login_id": "a username",' \
#                                '"password": "a password",' \
#                                '"team": "a team",' \
#                                '"channel": "a channel",' \
#                                '"room_id": "a room_id"}'
#
#         class MockGetDriver:
#             def __init__(self):
#                 self.client = self
#                 self.teams = self
#                 self.channels = self
#                 self.token = 'an access token'
#
#             def login(self, *args):
#                 pass
#
#             def get_team_by_name(self, *args):
#                 return {'id': 'a team id'}
#
#             def get_channel_by_name(self, *args):
#                 return {'id': 'a channel id'}
#
#             def init_websocket(self, *args):
#                 pass
#
#         get_driver.return_value = MockGetDriver()
#         store.return_value = None
#         res = self.client.post(self.endpoint, headers={self.http_auth_token_header: self.auth_token})
#         decrypt.assert_called_once()
#         get_driver.assert_called_once()
#         store.assert_called_once()
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertIsNone(res.data)
#
#     def test_no_token(self):
#         res = self.client.post(self.endpoint)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data, {'message': 'HTTP_AUTH_TOKEN header not found'})
#
#     @mock.patch('proxy.views.decrypt')
#     def test_invalid_token_data(self, decrypt):
#         decrypt.return_value = b'im not json'
#         res = self.client.post(path=self.endpoint, headers={self.http_auth_token_header: self.auth_token})
#         decrypt.assert_called_once()
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data, {'message': 'received invalid token'})
#
#     # @mock.patch.object(json, 'loads')
#     @mock.patch('proxy.views.decrypt')
#     def test_no_team_channel(self, decrypt):
#         decrypt.return_value = b'{}'
#         res = self.client.post(path=self.endpoint, headers={self.http_auth_token_header: self.auth_token})
#         decrypt.assert_called_once()
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data, {'message': 'team, channel or room_id not provided'})
#
#     @mock.patch('proxy.views.decrypt')
#     @mock.patch('proxy.views.get_driver')
#     def test_no_username_password(self, get_driver, decrypt):
#         decrypt.return_value = '{"team": "a team",' \
#                                '"channel": "a channel",' \
#                                '"room_id": "a room_id"}'
#         get_driver.return_value = None
#         res = self.client.post(self.endpoint, headers={self.http_auth_token_header: self.auth_token})
#         decrypt.assert_called_once()
#         get_driver.assert_called_once()
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# class MessageView(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.room_id = 'a5cd2d78-da25-49c2-a610-d2636bf58242'
#         self.endpoint = '/api/v1/rooms/{room_id}/messages/'.format(room_id=self.room_id)
#         self.payload = {'message': 'This is a message from a room.'}
#
#     @mock.patch('proxy.views.drivers', sample_driver)
#     def test_success(self):
#         res = self.client.post(path=self.endpoint, data=self.payload)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertIsNone(res.data)
#
#     @mock.patch('proxy.views.drivers', {})
#     def test_unauthorized(self):
#         res = self.client.post(path=self.endpoint, data=self.payload)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertIsNone(res.data)
#
#     @mock.patch('proxy.views.drivers', sample_driver)
#     def test_empty_message(self):
#         res = self.client.post(path=self.endpoint, data={'message': '   '})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data, {'message': 'message is empty'})
#
#     @mock.patch('proxy.views.drivers', sample_driver)
#     def test_no_message(self):
#         res = self.client.post(path=self.endpoint)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data, {'message': 'message not found'})
#
# #     # TODO test for 400, 401, 403 and requests exceptions
