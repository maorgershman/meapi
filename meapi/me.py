from meapi.account import Account
from meapi.auth import Auth
from meapi.exceptions import MeException
from meapi.notifications import Notifications
from meapi.settings import Settings
from meapi.social import Social
from meapi.util import Util


class Me(Auth, Account, Social, Settings, Notifications, Util):
    def __init__(self,
                 phone_number: int = None,
                 access_token: str = None,
                 uuid: str = None,
                 config_file: str = 'config.json',
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
        self.uuid = uuid
        self.phone_number = self.valid_phone_number(phone_number) if phone_number else phone_number
        self.proxies = proxies

        if not self.access_token:
            auth_data = self.credentials_manager()
            if auth_data:
                self.access_token = auth_data['access']
