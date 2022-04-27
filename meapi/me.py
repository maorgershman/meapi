from re import match
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
    Create a new instance to interact with MeAPI. **See** `Authentication <https://meapi.readthedocs.io/en/latest/setup.html#authentication>`_ **for more information.**

    :param phone_number: International phone number format. Required on the `Unofficial method <https://meapi.readthedocs.io/en/latest/setup.html#unofficial-method>`_. Default: ``None``.
    :type phone_number: Union[str, int, None]
    :param activation_code: You can provide the ``activation_code`` from Me in advance, without the need for a prompt. Default = ``None``.
    :type activation_code: Union[int, str, None]
    :param access_token: Official access token, Required on the `Official method <https://meapi.readthedocs.io/en/latest/setup.html#official-method>`_. Default: ``None``.
    :type access_token: Union[str, None]
    :param config_file: Path to credentials json file. Default: ``config.json``.
    :type config_file: Union[str, None]
    :param proxies: Dict with proxy configuration. Default: ``None``.
    :type proxies: dict
    :param account_details: You can provide all login details can be provided in dict format, designed for cases of new account registration without the need for a prompt. Default: ``None``
    :type account_details: dict

    Example for ``account_details``::

        {
            'phone_number': 972123456789, # Required always
            'activation_code': 123456, # Required only for the first time
            'first_name': 'Regina', # Required for first account registration
            'last_name': 'Phalange', # Optional for first account registration
            'email': 'kenadams@friends.tv', # Optional for first account registration
            'upload_random_data': True # Recommended for first account registration. Default: True
        }
    """
    def __init__(self,
                 phone_number: Union[int, str, None] = None,
                 activation_code: Union[int, str, None] = None,
                 access_token: Union[str, None] = None,
                 account_details: dict = None,
                 config_file: Union[str, None] = 'config.json',
                 proxies: dict = None):
        if config_file.endswith(".json"):
            self.config_file = config_file
        else:
            print("Not a valid config json file. Using default 'config.json' file.")
            self.config_file = 'config.json'

        if not access_token and not phone_number and not account_details:
            raise MeException("You need to provide phone number, account details or access token!")
        if access_token and phone_number:
            raise MeException("Access-token mode does not accept phone number, just access token.")
        if account_details and (phone_number or access_token):
            raise MeException("No need to provide phone number or access token if account_detail provided.")

        if account_details:
            if not isinstance(account_details, dict):
                raise MeException("Account details must be data dict. ")
            if account_details.get('phone_number') and account_details.get('activation_code'):
                phone_number = account_details['phone_number']
                if match(r'^\d{6}$', str(account_details['activation_code'])):
                    activation_code = account_details['activation_code']
                else:
                    raise MeException("Not a valid 6-digits activation code!")

        self.phone_number = self.valid_phone_number(phone_number) if phone_number else phone_number
        self.activation_code = activation_code
        self.access_token = access_token
        self.account_details = account_details
        self.uuid = None
        self.proxies = proxies

        if not self.access_token:
            auth_data = self.credentials_manager()
            if auth_data:
                self.access_token = auth_data['access']
