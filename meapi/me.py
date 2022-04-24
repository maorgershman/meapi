from typing import Union
from meapi.account import Account
from meapi.auth import Auth
from meapi.exceptions import MeException
from meapi.notifications import Notifications
from meapi.settings import Settings
from meapi.social import Social
from meapi.util import Util


class Me(Auth, Account, Social, Settings, Notifications, Util):
    """
    Create a new instance to interact with MeAPI. See `Authentication <https://meapi.readthedocs.io/en/latest/setup.html#authentication>`_ for more information.

    :param phone_number: International phone number format. Required on the `Unofficial method <https://meapi.readthedocs.io/en/latest/setup.html#unofficial-method>`_. Default: ``None``.
    :type phone_number: Union[str, int, None]
    :param access_token: Official access token, Required on the `Official method <https://meapi.readthedocs.io/en/latest/setup.html#official-method>`_. Default: ``None``.
    :type access_token: Union[str, None]
    :param config_file: Path to credentials json file. Default: ``config.json``.
    :type config_file: Union[str, None]
    :param proxies: Dict with proxy configuration. Default: ``None``.
    :type proxies: dict
    """
    def __init__(self,
                 phone_number: Union[str, int, None] = None,
                 access_token: Union[str, None] = None,
                 config_file: Union[str, None] = 'config.json',
                 proxies: dict = None):
        if config_file.endswith(".json"):
            self.config_file = config_file
        else:
            print("Not a valid config json file. Using default 'config.json' file.")
            self.config_file = 'config.json'

        if not access_token and not phone_number:
            raise MeException("You need to provide phone number or access token!")
        if access_token and phone_number:
            raise MeException("Access-token mode does not accept phone number, just access token.")

        self.access_token = access_token
        self.uuid = None
        self.phone_number = self.valid_phone_number(phone_number) if phone_number else phone_number
        self.proxies = proxies

        if not self.access_token:
            auth_data = self.credentials_manager()
            if auth_data:
                self.access_token = auth_data['access']
