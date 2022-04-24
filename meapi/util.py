from json import loads
from re import match, sub
from typing import Union
from requests import patch, delete, put, get, post
from meapi.exceptions import MeException, MeApiException

ME_BASE_API = 'https://app.mobile.me.app'


class Util:
    def initialize_headers(self) -> dict:
        """
        Get default header requests
        :return: dict with headers
        """
        return {'accept-encoding': 'gzip', 'user-agent': 'okhttp/4.9.1',
                'content-type': 'application/json; charset=UTF-8'}

    def valid_phone_number(self, phone_number: Union[str, int]) -> int:
        """
        Check if phone number is valid and return it clean without spaces or spacial characters
        :param phone_number: phone number in global format
        :return: fixed phone number
        """
        if phone_number:
            phone_number = sub(r'[\D]', '', str(phone_number))
            if match(r"^\d{9,15}$", phone_number):
                return int(phone_number)
        raise MeException("Not a valid phone number! " + phone_number)

    def make_request(self, req_type: str, endpoint: str, body: dict = None, headers: dict = None, auth: bool = True) -> Union[dict, list]:
        """
        Make request to Me api and return the response
        :param req_type: post, get, put, patch, delete
        :param endpoint: api endpoint
        :param body:
        :param headers:
        :param auth: use access token or not
        :return: api response
        """
        url = ME_BASE_API + endpoint
        request_types = ['post', 'get', 'put', 'patch', 'delete']
        if req_type not in request_types:
            raise MeException("Request type not in requests type list!!\nAvailable types: " + ", ".join(request_types))
        if headers is None:
            headers = self.initialize_headers()
        max_rounds = 3
        while max_rounds != 0:
            max_rounds -= 1
            if headers and auth:
                headers['authorization'] = self.access_token
            if req_type == 'post':
                response = post(url=url, json=body, headers=headers, proxies=self.proxies)
            elif req_type == 'get':
                response = get(url=url, json=body, headers=headers, proxies=self.proxies)
            elif req_type == 'put':
                response = put(url=url, json=body, headers=headers, proxies=self.proxies)
            elif req_type == 'delete':
                response = delete(url=url, json=body, headers=headers, proxies=self.proxies)
            elif req_type == 'patch':
                response = patch(url=url, json=body, headers=headers, proxies=self.proxies)
            response_text = loads(response.text)
            if response.status_code == 403 and self.phone_number:
                self.generate_access_token()
                continue

            if response.status_code >= 400:
                raise MeApiException(response.status_code, response_text, response.reason)
            return response_text
        else:
            raise MeException(f"Error when trying to send a {req_type} request to {url}.")
