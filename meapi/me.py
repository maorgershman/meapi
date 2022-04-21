from os import path, sep
from meapi.account import Account
from meapi.auth import Auth
from meapi.notifications import Notifications
from meapi.settings import Settings
from meapi.social import Social
from meapi.util import Util


class Me(Auth, Account, Social, Settings, Notifications, Util):
    def __init__(self,
                 phone_number: int,
                 access_token: str = None,
                 uuid: str = None,
                 config_file: str = None,
                 proxies: dict = None):

        if not config_file or not config_file.endswith(".json"):
            self.config_file = path.dirname(path.realpath(__file__)) + sep + 'config.json'
        else:
            self.config_file = config_file

        self.access_token = access_token
        self.uuid = uuid
        self.phone_number = self.valid_phone_number(phone_number)
        self.proxies = proxies

        if not self.access_token:
            auth_data = self.credentials_manager()
            if auth_data:
                self.access_token = auth_data['access']
