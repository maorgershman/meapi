from re import match
from typing import Union, List, Tuple
from meapi.exceptions import MeException, MeApiException


class Account:

    def phone_search(self, phone_number: Union[str, int]) -> Union[dict, None]:
        """
        Get basic information on phone number
        :param phone_number:
        :return: dict with data
        :example: existing_user - https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-phone_search_existed_user-py
        :example: non_user - https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-phone_search_non_user-py
        """
        try:
            response = self.make_request(req_type='get', endpoint='/main/contacts/search/?phone_number=' + str(self.valid_phone_number(phone_number)))
        except MeApiException as err:
            if err.http_status == 404 and err.msg['detail'] == 'Not found.':
                return None
        return response

    def get_profile_info(self, uuid: str = None) -> dict:
        """
        For Me users (those who have opened an account in the app) there is an account UUID obtained when receiving
         information about the phone number (me_obj.phone_search(phone_number)). With it, you can get social
         information and perform social actions.
        :param uuid: id of Me user. if none - get self profile
        :return: dict with details
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-profile-py
        """
        if uuid:
            return self.make_request('get', '/main/users/profile/' + str(uuid))
        return self.make_request('get', '/main/users/profile/me/')

    def get_uuid(self, phone_number: Union[int, str] = None) -> str:
        """
        Get user uuid
        :param phone_number: if none, return self uuid
        :return: string of uuid
        """
        if phone_number:
            return self.phone_search(phone_number).get('contact').get('uuid')
        try:
            return self.get_profile_info()['uuid']
        except MeApiException as err:
            if err.http_status == 401 and err.msg['detail'] == "User not found" and not self.uuid:  # on login, if no active account on this number
                print("** This is a new account and you need to register first.")
                first_name = input("* Enter your first name: ")
                last_name = input("* Enter your last name: ")
                email = input("* Enter your email: ")
                self.update_profile_info(first_name=first_name, last_name=last_name, email=email, login_type='email')
                return self.get_uuid()

    def update_profile_info(self, country_code: str = None,
                            date_of_birth: str = None,
                            device_type: str = None,
                            login_type: str = None,
                            email: str = None,
                            facebook_url: str = None,
                            first_name: str = None,
                            last_name: str = None,
                            gender: str = None,
                            profile_picture_url: str = None,
                            slogan: str = None) -> Tuple[bool, list]:
        """
        Update profile info
        :param login_type: email
        :param country_code: Your phone number country_code (972 = IL etc.)
        :param date_of_birth: YYYY-MM-DD format
        :param device_type: android/ios
        :param email: name@domian.com
        :param facebook_url: facebook id, for example 24898745174639
        :param first_name: first name
        :param last_name: last name
        :param gender: 'M' for male, 'F' for and 'N' for null
        :param profile_picture_url: direct image url
        :param slogan: bio
        :return: (is update success, list of failed)
        """
        device_types = ['android', 'ios']
        genders = {'M': 'M', 'F': 'F', 'N': None}
        body = {}
        if country_code is not None:
            body['country_code'] = str(country_code).upper()[:2]
        if not match(r"^\d{4}(\-)([0-2][0-9]|(3)[0-1])(\-)(((0)[0-9])|((1)[0-2]))$", str(date_of_birth)):
            raise MeException("Date of birthday must be in YYYY-MM-DD format!")
        if date_of_birth is not None:
            body['date_of_birth'] = str(date_of_birth)
        if str(device_type) in device_types:
            body['device_type'] = str(device_type)
        if login_type is not None:
            body['login_type'] = str(login_type)
        if match(r"^\S+@\S+\.\S+$", str(email)):
            body['email'] = str(email)
        if match(r"^\d+$", str(facebook_url)):
            body['facebook_url'] = str(facebook_url)
        if first_name is not None:
            body['first_name'] = str(first_name)
        if last_name is not None:
            body['last_name'] = str(last_name)
        if gender is not None and str(gender).upper() in genders.keys():
            body['gender'] = genders.get(str(gender.upper()))
        if match(r"(https?:\/\/.*\.(?:png|jpg))", str(profile_picture_url)):
            body['profile_picture'] = profile_picture_url
        if slogan is not None:
            body['slogan'] = str(slogan)

        if not body:
            raise MeException("You must change at least one detail!")

        results = self.make_request('patch', '/main/users/profile/', body)
        failed = []
        for key in body.keys():
            if results[key] != body[key] and key != 'profile_picture':
                # Can't check if profile picture updated because Me convert's it to their own url.
                # you can check before and after.. get_settings()
                failed.append(key)
        return not bool(failed), failed

    # def upload_profile_picture(self, image_path):
    #     headers = {'content-type': 'multipart/form-data; boundary=7ffe4aca-db30-4d2a-921b-a14490a8e0a4'}
    #     endpoint = '/media/file/upload/'

    def delete_account(self) -> bool:
        """
        Delete your account and it's data (!!!)
        :return: is deleted
        """
        return True if not self.make_request('delete', '/main/settings/remove-user/') else False

    def suspend_account(self) -> bool:
        """
        Suspend your account until your next login.
        :return: is suspended
        """
        return self.make_request('put', '/main/settings/suspend-user/')['contact_suspended']

    @staticmethod
    def contacts(contacts: List[dict]) -> List[dict]:
        contacts_list = []
        for contact in contacts:
            if isinstance(contact, dict):
                if contact.get('name') and contact.get('phone_number'):
                    contacts_list.append(contact)
        if not contacts_list:
            raise MeException("Valid contacts not found! check this example for valid contact syntax: "
                              "https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-contacts-py")
        return contacts_list

    def add_contacts(self, contacts: List[dict]):
        """
        Upload contacts to your Me account
        :param contacts: [{
            "country_code": "IL",
            "date_of_birth": null,
            "name": "Jonathan",
            "phone_number": 987546787327}]
        :return: dict with upload results
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-contacts-py
        """
        body = {"add": self.contacts(contacts), "is_first": False, "remove": []}
        return self.make_request('post', '/main/contacts/sync/', body)

    def remove_contacts(self, contacts: List[dict]):
        """
        Upload contacts to your Me account
        :param contacts: [{
            "country_code": "IL",
            "date_of_birth": null,
            "name": "Jonathan",
            "phone_number": 987546787327}]
        :return: dict with upload results
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-contacts-py
        """
        body = {"add": [], "is_first": False, "remove": self.contacts(contacts)}
        return self.make_request('post', '/main/contacts/sync/', body)

    @staticmethod
    def calls(calls: List[dict]) -> List[dict]:
        calls_list = []
        for call in calls:
            if isinstance(call, dict):
                if not call.get('name') or not call.get('phone_number'):
                    if call.get('phone_number'):
                        call['name'] = str(call.get('phone_number'))
                    else:
                        raise MeException("Phone number must be provided!!")
                if call.get('type') not in ['incoming', 'missed', 'outgoing']:
                    raise MeException("No such call type as " + str(call.get('type')) + "!")
                if not call.get('duration'):
                    call['duration'] = 123
                if not call.get('tag'):
                    call['tag'] = None
                if not call.get('called_at'):
                    call['called_at'] = '2022-04-18T05:59:07Z'
                    calls_list.append(call)
        if not calls_list:
            raise MeException("Valid calls not found! check this example for valid call syntax: "
                              "https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-calls_log-py")
        return calls_list

    def add_calls_to_log(self, calls: List[dict]):
        """
        Add call to your calls log
        :param calls: [{
          "called_at": "2021-07-29T11:27:50Z",
          "duration": 0,
          "name": "John",
          "phone_number": 9843437535,
          "tag": null,
          "type": "missed"}]
        :return: dict with upload result
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-calls_log-py
        """
        body = {"add": self.calls(calls), "remove": []}
        return self.make_request('post', '/main/call-log/change-sync/', body)

    def remove_calls_from_log(self, calls: List[dict]):
        """
        Add call to your calls log
        :param calls: [{
          "called_at": "2021-07-29T11:27:50Z",
          "duration": 0,
          "name": "John",
          "phone_number": 9843437535,
          "tag": null,
          "type": "missed"}]
        :return: dict with upload result
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-calls_log-py
        """
        body = {"add": [], "remove": self.calls(calls)}
        return self.make_request('post', '/main/call-log/change-sync/', body)

    def block_profile(self, phone_number: int, block_contact=True, me_full_block=True) -> bool:
        """
        Block user profile
        :param phone_number: user phone number
        :param block_contact: block for calls
        :param me_full_block: block for social
        :return: is blocking success
        """
        body = {"block_contact": block_contact, "me_full_block": me_full_block,
                "phone_number": str(self.valid_phone_number(phone_number))}
        return self.make_request('post', '/main/users/profile/block/', body)['success']

    def unblock_profile(self, phone_number: int, block_contact=False, me_full_block=False) -> bool:
        """
        Unblock user profile
        :param phone_number: user phone number
        :param block_contact: unblock from calls
        :param me_full_block: unblock for social
        :return: is unblocked success
        """
        body = {"block_contact": block_contact, "me_full_block": me_full_block,
                "phone_number": str(self.valid_phone_number(phone_number))}
        return self.make_request('post', '/main/users/profile/block/', body)['success']

    def block_numbers(self, numbers: Union[int, List[int]]) -> bool:
        """
        Block numbers
        :param numbers: phone number/s
        :return: is blocking success
        """
        if not isinstance(numbers, list):
            numbers = [numbers]
        body = {"phone_numbers": numbers}
        return self.make_request('post', '/main/users/profile/bulk-block/', body)['block_contact']

    def unblock_numbers(self, numbers: Union[int, List[int]] = None) -> bool:
        """
        Unblock numbers
        :param numbers: phone number/s
        :return: is unblocked success
        """
        if not isinstance(numbers, list):
            numbers = [numbers]
        body = {"phone_numbers": numbers}
        return self.make_request('post', '/main/users/profile/bulk-unblock/', body)['success']

    def get_blocked_numbers(self) -> List[dict]:
        """
        Get list of blocked numbers
        :return: list of dicts
        """
        return self.make_request('get', '/main/settings/blocked-phone-numbers/')

    def update_location(self, lat: float, lon: float) -> bool:
        """
        Update user location
        :param lat: location latitude
        :param lon: location longitude
        :return: is location update success
        """
        if not isinstance(lat, float) or not isinstance(lon, float):
            raise Exception("Not a valid coordination!")
        body = {"location_latitude": float(lat), "location_longitude": float(lon)}
        return self.make_request('post', '/main/location/update/', body)['success']

    def upload_sample_data(self):
        try:
            from sample_data import calls_log, contacts, location_coordinates
        except ImportError:
            raise Exception("Sample data file is missing.")
        self.update_location(*location_coordinates.values())
        self.add_contacts(contacts)
        self.add_calls_to_log(calls_log)
