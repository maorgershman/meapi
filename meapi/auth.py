from json import load, JSONDecodeError, dump
from os import path
from re import match
from typing import Union
from meapi.exceptions import MeException, MeApiException

wa_auth_url = "https://wa.me/972543229534?text=Connectme"
tg_auth_url = "http://t.me/Meofficialbot?start=__iw__{}"


class Auth:
    def activate_account(self, activation_code: Union[int, str, None] = None) -> bool:
        """
        Activate new phone number account.

        :param activation_code: You can pass the activation code if you want to skipp the prompt. Default: ``None``.
        :type activation_code: Union[int, str, None]
        :raises MeException: If pre-activation-code is not valid.
        :raises MeApiException: msg: ``api_incorrect_activation_code`` If activation-code is incorrect.
        :return: Is success.
        :rtype: bool
        """
        if not activation_code and self.activation_code:
            activation_code = self.activation_code

        if activation_code and not match(r'^\d{6}$', str(activation_code)):
            raise MeException("Not a valid 6-digits activation code!")
        if not activation_code:
            print(f"To get access token you need to authorize yourself:"
                  f"\n* WhatsApp (Recommended): {wa_auth_url}\n* Telegram: {tg_auth_url.format(self.phone_number)}\n")
        while not activation_code:
            activation_code = input("** Enter your verification code (6 digits): ")
            while not match(r'^\d{6}$', str(activation_code)):
                activation_code = input("** Incorrect code. The verification code includes 6 digits. Please enter: ")
        data = {
            "activation_code": str(activation_code),
            "activation_type": "sms",
            "phone_number": int(self.phone_number)
        }
        try:
            print("** Trying to verify...")
            results = self.make_request(req_type='post', endpoint='/auth/authorization/activate/', body=data, auth=False)
            if results.get('access'):
                access_token = results['access']
            else:
                raise MeException(str(results))
        except MeApiException as err:
            if err.http_status == 400 and err.msg == 'api_incorrect_activation_code':
                err.reason = "Wrong activation code!"
            raise err

        if access_token:
            print("Verification completed.")
            self.access_token = access_token
            self.credentials_manager(results)
            return True
        else:
            return False

    def generate_access_token(self) -> bool:
        """
        Generate new access token.

        :raises MeApiException: msg: ``api_incorrect_pwd_token`` if ``pwd_token`` is broken.
        :return: is success.
        :type: bool
        """
        auth_data = self.credentials_manager()
        if not auth_data:
            if self.activate_account():
                return True
        body = {"phone_number": str(self.phone_number),
                "pwd_token": auth_data['pwd_token']}
        print("Generating new access token...")
        try:
            auth_data = self.make_request(req_type='post', endpoint='/auth/authorization/login/', body=body, auth=False)
        except MeApiException as err:
            if err.http_status == 400 and err.msg == 'api_incorrect_pwd_token':
                err.reason = f"Your pwd_token in {self.config_file} is broken (You probably activated the account elsewhere)."
            raise err
        access_token = auth_data['access']
        if access_token:
            print("Success to generate new token.")
            self.access_token = access_token
            self.credentials_manager(auth_data)
            return True
        return False

    def credentials_manager(self, data: Union[dict, None] = None) -> dict:
        """
        Read / write auth data from ``config_file``.

        :param data: Dict with ``access``, ``refresh`` and ``pwd_token``. Default: ``None``.
        :type data: Union[dict, None]
        :raises MeException: If the json file is broken or if the provided data not contains ``access`` or ``refresh`` token.
        :return: Dict with auth data.
        :rtype: dict
        """
        if not path.isfile(str(self.config_file)):
            with open(self.config_file, "w") as new_config_file:
                new_config_file.write('{}')

        with open(self.config_file, "r") as config_file:
            try:
                existing_content = load(config_file)
            except JSONDecodeError:
                raise MeException("Not a valid json file: " + self.config_file)
        if not data:
            if not existing_content.get(str(self.phone_number)):
                if self.activate_account():
                    return self.credentials_manager()
            else:
                existing_content = existing_content.get(str(self.phone_number))
                self.uuid = existing_content['uuid']
                return existing_content
        else:
            if not data.get('access') or not data.get('refresh'):
                raise MeException(f"Wrong data provided! {data}")

            pwd_token = None
            if existing_content:
                if existing_content.get(str(self.phone_number)):
                    pwd_token = existing_content.get(str(self.phone_number)).get('pwd_token')
            uuid = self.get_uuid()
            self.uuid = uuid
            existing_content[str(self.phone_number)] = data
            existing_content[str(self.phone_number)]['uuid'] = uuid
            if pwd_token and not data.get('pwd_token'):
                existing_content[str(self.phone_number)]['pwd_token'] = pwd_token

            with open(self.config_file, "w") as config_file:
                dump(existing_content, config_file, indent=4, sort_keys=True)
            return existing_content[str(self.phone_number)]
