from json import loads, JSONDecodeError
from re import match, sub
from typing import Union
from requests import patch, delete, put, get, post
from meapi.exceptions import MeException, MeApiException

ME_BASE_API = 'https://app.mobile.me.app'


class Util:

    def valid_phone_number(self, phone_number: Union[str, int]) -> int:
        """
        Check if phone number is valid and return it clean without spaces, pluses or other spacial characters.
         - ``(972) 123-4567890``, ``+9721234567890``, ``123-456-7890`` --> ``9721234567890``.

        :param phone_number: phone number in global format.
        :type phone_number: Union[int, str]
        :raises MeException: If length of phone number not between 9-15.
        :return: fixed phone number
        :rtype: int
        """
        if phone_number:
            phone_number = sub(r'[\D]', '', str(phone_number))
            if match(r"^\d{9,15}$", phone_number):
                return int(phone_number)
        raise MeException("Not a valid phone number! " + phone_number)

    def make_request(self,
                     req_type: str,
                     endpoint: str,
                     body: dict = None,
                     headers: dict = None,
                     auth: bool = True
                     ) -> Union[dict, list]:
        """
        Make request to Me api and return the response.

        :param req_type: HTTP request type: ``post``, ``get``, ``put``, ``patch``, ``delete``.
        :type req_type: str
        :param endpoint: api endpoint.
        :type endpoint: str
        :param body: The body of the request. Default: ``None``.
        :type body: dict
        :param headers: Use different headers instead of the default.
        :type headers: dict
        :param auth: Do use access token in this request? Default: ``True``.
        :raises MeApiException: If HTTP status is bigger than ``400``.
        :return: API response as dict or list.
        :rtype: Union[dict, list]
        """
        url = ME_BASE_API + endpoint
        request_types = ['post', 'get', 'put', 'patch', 'delete']
        if req_type not in request_types:
            raise MeException("Request type not in requests type list!!\nAvailable types: " + ", ".join(request_types))
        if headers is None:
            headers = {'accept-encoding': 'gzip', 'user-agent': 'okhttp/4.9.1',
                       'content-type': 'application/json; charset=UTF-8'}
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
            try:
                response_text = loads(response.text)
            except JSONDecodeError:
                raise MeException(f"The response (Status code: {response.status_code}) received does not contain a valid JSON:\n" + str(response.text))
            if response.status_code == 403 and self.phone_number:
                self.generate_access_token()
                continue

            if response.status_code >= 400:
                raise MeApiException(response.status_code, str(response_text.get('detail') or response_text.get('phone_number') or response_text), response.reason)
            return response_text
        else:
            raise MeException(f"Error when trying to send a {req_type} request to {url}, with body:\n{body} and with headers:\n{headers}.")
