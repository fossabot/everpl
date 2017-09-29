# Include standard modules
import unittest
from unittest import mock
import asyncio
import json
import xml

# Include 3rd-party modules
import aiohttp

# Include DPL modules
from dpl.api import ApiGateway
from dpl.api import exceptions
from dpl.api import api_errors

from dpl.api.rest_api import RestApi


class TestRestApiProvider(unittest.TestCase):
    host = "localhost"
    port = 19101
    base_url = "http://{0}:{1}/".format(host, port)

    def setUp(self):
        # create a new event loop
        self.loop = asyncio.new_event_loop()  # type: asyncio.AbstractEventLoop

        # create a mock of ApiGateway
        self.api_gateway_mock = mock.Mock(spec_set=ApiGateway)

        # create an instance of RestApi
        self.rest_api_provider = RestApi(
            self.api_gateway_mock,
            self.loop
        )

        # TODO: Pick a random free port. Check if port is free
        # create rest server on localhost and specified port
        self.loop.run_until_complete(
            self.rest_api_provider.create_server(
                host=self.host, port=self.port
            )
        )

    def tearDown(self):
        # shutdown rest server
        self.loop.run_until_complete(
            self.rest_api_provider.shutdown_server()
        )

        # close old event loop
        self.loop.close()

        # delete links to used objects
        del self.rest_api_provider
        del self.api_gateway_mock

        del self.loop

    def test_root(self):
        test_response_body = {
            "things": "/things/",
            "auth": "/auth",
            "messages": "/messages/",
            "placements": "/placements/"
        }

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.get(self.base_url) as resp:
                    self.assertEqual(resp.status, 200)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_success(self):
        test_url = self.base_url + 'auth'

        test_token = "asdfghjkl"
        test_request_body = json.dumps({
            "username": "nobody cares",
            "password": "nobody cares"
        })
        test_request_headers = {'content-type': 'application/json'}

        test_response_body = {
            "token": test_token,
            "message": "authorized"
        }

        self.api_gateway_mock.auth = mock.Mock()
        self.api_gateway_mock.auth.return_value = test_token

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, data=test_request_body, headers=test_request_headers) as resp:
                    self.assertEqual(resp.status, 200)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_content_header_missing(self):
        test_url = self.base_url + 'auth'

        test_request_body = {
            "username": "nobody cares",
            "password": "nobody cares"
        }
        test_request_headers = {}

        test_response_body = api_errors.ERROR_TEMPLATES[1000].to_dict()
        test_response_status = 400

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, data=test_request_body, headers=test_request_headers) as resp:
                    self.assertEqual(resp.status, test_response_status)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_body_decode_failed(self):
        test_url = self.base_url + 'auth'

        test_request_body = json.dumps({
            "username": "nobody cares",
            "password": "nobody cares"
        })
        test_request_body = "{" + test_request_body  # append an extra bracket and make json invalid
        test_request_headers = {'content-type': 'application/json'}

        test_response_body = api_errors.ERROR_TEMPLATES[1001].to_dict()
        test_response_status = 400

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, data=test_request_body, headers=test_request_headers) as resp:
                    self.assertEqual(resp.status, test_response_status)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_username_missing(self):
        test_url = self.base_url + 'auth'

        test_request_body = {
            "password": "nobody cares"
        }

        test_response_body = api_errors.ERROR_TEMPLATES[2000].to_dict()
        test_response_status = 400

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, json=test_request_body) as resp:
                    self.assertEqual(resp.status, test_response_status)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_password_missing(self):
        test_url = self.base_url + 'auth'

        test_request_body = {
            "username": "nobody cares"
        }

        test_response_body = api_errors.ERROR_TEMPLATES[2001].to_dict()
        test_response_status = 400

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, json=test_request_body) as resp:
                    self.assertEqual(resp.status, test_response_status)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

    def test_auth_bad_username_password_combination(self):
        test_url = self.base_url + 'auth'

        test_request_body = {
            "username": "nobody cares",
            "password": "nobody cares"
        }

        def auth_side_effect(*args, **kwargs):
            # FIXME: specify more concrete exception
            raise ValueError()

        test_response_body = api_errors.ERROR_TEMPLATES[2002].to_dict()
        test_response_status = 401

        self.api_gateway_mock.auth = mock.Mock()
        self.api_gateway_mock.auth.side_effect = auth_side_effect

        async def body():
            async with aiohttp.ClientSession(loop=self.loop) as session:
                async with session.post(test_url, json=test_request_body) as resp:
                    self.assertEqual(resp.status, test_response_status)
                    self.assertEqual(await resp.json(), test_response_body)

        self.loop.run_until_complete(body())

if __name__ == '__main__':
    unittest.main()
