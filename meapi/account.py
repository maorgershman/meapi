from re import match
from typing import Union, List, Tuple
from meapi.exceptions import MeException, MeApiException
from meapi.random_data import get_random_data
from random import randint


def validate_contacts(contacts: List[dict]) -> List[dict]:
    """
    Gets list of dict of contacts and return the valid contacts in the same format. to use of add_contacts and remove_contacts methods
    """
    contacts_list = []
    for contact in contacts:
        if isinstance(contact, dict):
            if contact.get('name') and contact.get('phone_number'):
                contacts_list.append(contact)
    if not contacts_list:
        raise MeException("Valid contacts not found! check this example for valid contact syntax: "
                          "https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-contacts-py")
    return contacts_list


def validate_calls(calls: List[dict]) -> List[dict]:
    """
    Gets list of dict of calls and return the valid calls in the same format. to use of add_calls_to_log and remove_calls_from_log methods
    """
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
                call['duration'] = randint(10, 300)
            if not call.get('tag'):
                call['tag'] = None
            if not call.get('called_at'):
                call['called_at'] = f"{randint(2018, 2022)}-{randint(1, 12)}-{randint(1, 31)}T{randint(1, 23)}:{randint(10, 59)}:{randint(10, 59)}Z"
            calls_list.append(call)
    if not calls_list:
        raise MeException("Valid calls not found! check this example for valid call syntax: "
                          "https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-calls_log-py")
    return calls_list


class Account:

    def phone_search(self, phone_number: Union[str, int]) -> dict:
        """
        Get information on any phone number.

        :param phone_number: International phone number format.
        :type phone_number: Union[str, int])
        :raises MeApiException: msg: ``api_search_passed_limit`` if you passed the limit (About 350 per day in the unofficial auth method).
        :return: Dict with information about the phone number.
        :rtype: dict

        Example for existed user::

            {
                "contact": {
                    "name": "Chandler bing",
                    "picture": None,
                    "user": {
                        "email": "user@domain.com",
                        "profile_picture": "https://d18zaexXXp1s.cloudfront.net/5XXX971XXXXXXXXXfa67.jpg",
                        "first_name": "Chandler",
                        "last_name": "Bing",
                        "gender": 'M',
                        "uuid": "XXXXX-XXXX-XXXX-XXXX-XXXX",
                        "is_verified": True,
                        "phone_number": 7434872457,
                        "slogan": "User bio",
                        "is_premium": False,
                        "verify_subscription": True,
                        "id": 42453345,
                        "comment_count": 0,
                        "location_enabled": False,
                        "distance": None,
                    },
                    "suggested_as_spam": 0,
                    "is_permanent": False,
                    "is_pending_name_change": False,
                    "user_type": "BLUE",
                    "phone_number": 7434872457,
                    "cached": True,
                    "is_my_contact": False,
                    "is_shared_location": False,
                }
            }

        Example for non user::

            {
                "contact": {
                    "name": "Chandler bing",
                    "picture": None,
                    "user": None,
                    "suggested_as_spam": 0,
                    "is_permanent": False,
                    "is_pending_name_change": False,
                    "user_type": "GREEN",
                    "phone_number": 123456789,
                    "cached": False,
                    "is_my_contact": False,
                    "is_shared_location": False,
                }
            }
        """
        try:
            response = self.make_request(req_type='get', endpoint='/main/contacts/search/?phone_number=' + str(
                self.valid_phone_number(phone_number)))
        except MeApiException as err:
            if err.http_status == 404 and err.msg == 'Not found.':
                return {}
            else:
                raise err
        return response

    def get_profile_info(self, uuid: str = None) -> dict:
        """
        For Me users (those who have registered in the app) there is an account UUID obtained when receiving
        information about the phone number :py:func:`phone_search`. With it, you can get social information
        and perform social actions.

        :param uuid: uuid of the Me user. Default: your uuid.
        :type uuid: str
        :raises MeApiException: msg: ``api_profile_view_passed_limit`` if you passed the limit (About 500 per day in the unofficial auth method).
        :return: Dict with profile details
        :rtype: dict

        Example::

            {
                "comments_blocked": False,
                "is_he_blocked_me": False,
                "is_permanent": False,
                "is_shared_location": False,
                "last_comment": None,
                "mutual_contacts_available": True,
                "mutual_contacts": [
                    {
                        "phone_number": 1234567890,
                        "name": "Ross geller",
                        "referenced_user": {
                            "email": "rossgeller@friends.com",
                            "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/59XXXXXXXXXXXXXXXX67.jpg",
                            "first_name": "Ross",
                            "last_name": "",
                            "gender": 'M',
                            "uuid": "XXXX-XXX-XXX-83c1-XXXX",
                            "is_verified": True,
                            "phone_number": 3432434546546,
                            "slogan": "Pivot!",
                            "is_premium": False,
                            "verify_subscription": True,
                        },
                        "date_of_birth": '1980-03-13',
                    }
                ],
                "profile": {
                    "carrier": "XXX mobile",
                    "comments_enabled": False,
                    "country_code": "XX",
                    "date_of_birth": '2222-05-20',
                    "device_type": "android",
                    "distance": None,
                    "email": "user@domain.com",
                    "facebook_url": "133268763438473",
                    "first_name": "Chandler",
                    "gdpr_consent": True,
                    "gender": 'M',
                    "google_url": None,
                    "is_premium": False,
                    "is_verified": True,
                    "last_name": "Bing",
                    "location_enabled": False,
                    "location_name": "XXXX",
                    "login_type": "email",
                    "me_in_contacts": True,
                    "phone_number": 123456789012,
                    "phone_prefix": "123",
                    "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/5XXX712a0676XXXXXXXfa67.jpg",
                    "slogan": "I will always be there for you",
                    "user_type": "BLUE",
                    "uuid": "XXXXXXXXXXXXXXXXXXX3c1-6932bc9eb597",
                    "verify_subscription": True,
                    "who_deleted_enabled": True,
                    "who_watched_enabled": True,
                },
                "share_location": False,
                "social": {
                    "facebook": {
                        "posts": [],
                        "profile_id": "https://www.facebook.com/app_scoped_user_id/XXXXXXXXXXX/",
                        "is_active": True,
                        "is_hidden": True,
                    },
                    "fakebook": {
                        "is_active": False,
                        "is_hidden": True,
                        "posts": [],
                        "profile_id": None,
                    },
                    "instagram": {
                        "posts": [
                            {
                                "posted_at": "2021-12-23T22:21:06Z",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/XXXXXXXXXXXXXX.jpg",
                                "text_first": None,
                                "text_second": "IMAGE",
                                "author": "username",
                                "redirect_id": "CXXXXIz-0",
                                "owner": "username",
                            }
                        ],
                        "profile_id": "username",
                        "is_active": True,
                        "is_hidden": False,
                    },
                    "linkedin": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [],
                        "profile_id": "https://www.linkedin.com/in/username",
                    },
                    "pinterest": {
                        "posts": [],
                        "profile_id": "https://pin.it/XXXXXXXX",
                        "is_active": True,
                        "is_hidden": False,
                    },
                    "spotify": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [
                            {
                                "author": "Chandler bing",
                                "owner": "4xgXXXXXXXt0pv",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/9bcXXXfa7dXXXXXXXac.jpg",
                                "posted_at": None,
                                "redirect_id": "4KgES5cs3SnMhuAXuBREW2",
                                "text_first": "My friends playlist songs",
                                "text_second": "157",
                            },
                            {
                                "author": "Chandler Bing",
                                "owner": "4xgoXcoriuXXXXpt0pv",
                                "photo": "https://d18zaexen4dp1s.cloudfront.net/55d3XXXXXXXXXXXXXXXXXX4.jpg",
                                "posted_at": None,
                                "redirect_id": "3FjSXXXCQPB14Xt",
                                "text_first": "My favorite songs!",
                                "text_second": "272",
                            },
                        ],
                        "profile_id": "4xgot8coriuXXXXXpt0pv",
                    },
                    "tiktok": {
                        "is_active": False,
                        "is_hidden": True,
                        "posts": [],
                        "profile_id": None,
                    },
                    "twitter": {
                        "is_active": True,
                        "is_hidden": False,
                        "posts": [
                            {
                                "author": "username",
                                "owner": "username",
                                "photo": "https://pbs.twimg.com/profile_images/13XXXXX76/AvBXXXX_normal.jpg",
                                "posted_at": "2021-08-24T10:02:45Z",
                                "redirect_id": "https://twitter.com/username/status/1XXXXXX423",
                                "text_first": "My tweet #1 https://t.co/PLXXXX2Tw https://t.co/zXXXXkk",
                                "text_second": None,
                            },
                            {
                                "author": "username",
                                "owner": "username",
                                "photo": "https://pbs.twimg.com/profile_images/1318XXXX0976/AvBXXXUk_normal.jpg",
                                "posted_at": "2021-08-12T10:09:23Z",
                                "redirect_id": "https://twitter.com/username/status/142XXXXX86624",
                                "text_first": "My second tweet https://t.co/xtqXXXtAC",
                                "text_second": None,
                            },
                        ],
                        "profile_id": "username",
                    },
                },
            }
        """
        if uuid:
            return self.make_request('get', '/main/users/profile/' + str(uuid))
        return self.make_request('get', '/main/users/profile/me/')

    def get_uuid(self, phone_number: Union[int, str] = None) -> Union[str, None]:
        """
        Get user's uuid (To use in :py:func:`get_profile_info`, :py:func:`get_comments` and more).

        :param phone_number: International phone number format. Default: None (Return self uuid).
        :type phone_number: Union[str, int, None]
        :return: String of uuid, or None if no user exists on the provided phone number.
        :rtype: Union[str, None]
        """
        if phone_number:
            res = self.phone_search(phone_number).get('contact').get('user')
            if res:
                return res.get('uuid')
            return None
        try:
            return self.get_profile_info()['uuid']
        except MeApiException as err:
            if err.http_status == 401:  # on login, if no active account on this number you need to register
                print("** This is a new account and you need to register first.")
                if self.account_details:
                    account_details: dict = self.account_details
                else:
                    account_details = {}
                print(account_details)
                first_name = None
                last_name = None
                email = None
                upload_random_data = None

                if account_details.get('first_name'):
                    first_name = account_details['first_name']
                else:
                    while not first_name:
                        first_name = input("* Enter your first name (Required): ")

                if account_details.get('last_name'):
                    last_name = account_details['last_name']
                elif not account_details:
                    last_name = input("* Enter your last name (Optional): ")

                if account_details.get('email'):
                    email = account_details['email']
                elif not account_details:
                    email = input("* Enter your email (Optional): ") or None

                if account_details.get('upload_random_data'):
                    upload_random_data = account_details['upload_random_data']
                elif not account_details:
                    answer = "X"
                    while answer.upper() not in ['Y', 'N', '']:
                        answer = input("* Do you want to upload some random data (contacts, calls, location) in order "
                                       "to initialize the account? (Enter is Y) [Y/N]: ")
                    if answer.upper() in ["Y", ""]:
                        upload_random_data = True
                    else:
                        upload_random_data = False

                results = self.update_profile_info(first_name=first_name, last_name=last_name, email=email, login_type='email')
                if results[0]:
                    msg = "** Your profile successfully created!"
                    if upload_random_data:
                        self.upload_random_data()
                        msg += "\n* But you may not be able to perform searches for a few hours. It my help to " \
                               "upload some data. You can use in me.upload_random_data() or other account methods to " \
                               "activate your account."
                    print(msg)
                    return self.get_uuid()
                raise MeException("Can't update the following details: " + ", ".join(results[1]))
            else:
                raise err

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
        Update profile information.

        :param login_type: ``email``. Default: ``None``
        :type login_type: str
        :param country_code: Your phone number country_code (``972`` = ``IL`` etc.) // `Country codes <https://countrycode.org/>`_. Default: ``None``
        :type country_code: str
        :param date_of_birth: ``YYYY-MM-DD`` format. for example: ``1997-05-15``. Default: ``None``
        :type date_of_birth: str
        :param device_type: ``android`` / ``ios``. Default: ``None``
        :type device_type: str
        :param email: For example: ``name@domian.com``. Default: ``None``
        :type email: str
        :param facebook_url: facebook id, for example: ``24898745174639``. Default: ``None``
        :type facebook_url: Union[str, int]
        :param first_name: First name. Default: ``None``
        :type first_name: str
        :param last_name: Last name. Default: ``None``
        :type last_name: str
        :param gender: ``M`` for male, ``F`` for and ``N`` for None. Default: ``None``
        :type gender: str
        :param profile_picture_url: Direct image url. for example: ``https://example.com/image.png``. Default: ``None``
        :type profile_picture_url: str
        :param slogan: Your bio. Default: ``None``
        :type slogan: str
        :return: Tuple of: is update success, list of failed.
        :rtype: Tuple[bool, list]
        """
        device_types = ['android', 'ios']
        genders = {'M': 'M', 'F': 'F', 'N': None}
        body = {}
        if country_code is not None:
            body['country_code'] = str(country_code).upper()[:2]
        if date_of_birth is not None:
            if not match(r"^\d{4}(\-)([0-2][0-9]|(3)[0-1])(\-)(((0)[0-9])|((1)[0-2]))$", str(date_of_birth)):
                raise MeException("Date of birthday must be in YYYY-MM-DD format!")
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
        if gender is not None:
            if str(gender).upper() in genders.keys():
                body['gender'] = genders.get(str(gender.upper()))
            else:
                raise MeException("Gender must be: 'F' for female, 'M' for Male, and 'N' for null.")
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

        :return: Is deleted.
        :rtype: bool
        """
        return True if not self.make_request('delete', '/main/settings/remove-user/') else False

    def suspend_account(self) -> bool:
        """
        Suspend your account until your next login.

        :return: is suspended.
        :rtype: bool
        """
        return self.make_request('put', '/main/settings/suspend-user/')['contact_suspended']

    def add_contacts(self, contacts: List[dict]):
        """
        Upload new contacts to your Me account. See :py:func:`upload_random_data`.

        :param contacts: List of dicts with contacts data.
        :type contacts: List[dict])
        :return: Dict with upload results.
        :rtype: dict

        Example of list of contacts to add::

            [
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Chandler",
                    "phone_number": 512145887,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Monica",
                    "phone_number": 512646807,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Rachel",
                    "phone_number": 503453530,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Phoebe",
                    "phone_number": 543244983,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Ross",
                    "phone_number": 556424247,
                },
                {
                    "country_code": "US",
                    "date_of_birth": None,
                    "name": "Joey",
                    "phone_number": 95353543327,
                },
            ]
        """
        body = {"add": validate_contacts(contacts), "is_first": False, "remove": []}
        return self.make_request('post', '/main/contacts/sync/', body)

    def get_saved_contacts(self) -> List[dict]:
        """
        Get all the contacts stored in your contacts (Which has an Me account).

        :return: List of dicts with all contacts data.
        :rtype: List[dict]
        """
        return [contact for group in self.get_groups_names['names'] for contact in group['contacts'] if contact['in_contact_list']]

    def get_unsaved_contacts(self) -> List[dict]:
        """
        Get all the contacts that not stored in your contacts (Which has an Me account).

        :return: List of dicts with all contacts data.
        :rtype: List[dict]
        """
        return [contact for group in self.get_groups_names['names'] for contact in group['contacts'] if not contact['in_contact_list']]

    def remove_contacts(self, contacts: List[dict]) -> dict:
        """
        Remove contacts from your Me account.

        :param contacts: List of dicts with contacts data.
        :type contacts: List[dict])
        :return: Dict with upload results.
        :rtype: dict

        Example of list of contacts to remove::

            [
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Chandler",
                    "phone_number": 512145887,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Monica",
                    "phone_number": 512646807,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Rachel",
                    "phone_number": 503453530,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Phoebe",
                    "phone_number": 543244983,
                },
                {
                    "country_code": "XX",
                    "date_of_birth": None,
                    "name": "Ross",
                    "phone_number": 556424247,
                },
                {
                    "country_code": "US",
                    "date_of_birth": None,
                    "name": "Joey",
                    "phone_number": 95353543327,
                },
            ]
        """
        body = {"add": [], "is_first": False, "remove": validate_contacts(contacts)}
        return self.make_request('post', '/main/contacts/sync/', body)

    def add_calls_to_log(self, calls: List[dict]) -> dict:
        """
        Add call to your calls log. See :py:func:`upload_random_data`.

        :param calls: List of dicts with calls data.
        :type calls: List[dict]
        :return: dict with upload result.
        :rtype: dict

        Example of list of calls to add::

            [
                {
                    "called_at": "2021-07-29T11:27:50Z",
                    "duration": 28,
                    "name": "043437535",
                    "phone_number": 43437535,
                    "tag": None,
                    "type": "missed",
                },
                {
                    "called_at": "2021-08-08T19:42:59Z",
                    "duration": 0,
                    "name": "Chandler",
                    "phone_number": 334324324,
                    "tag": None,
                    "type": "outgoing",
                },
                {
                    "called_at": "2022-01-03T16:50:24Z",
                    "duration": 15,
                    "name": "Joey",
                    "phone_number": 51495043537,
                    "tag": None,
                    "type": "incoming",
                },
            ]
        """
        body = {"add": validate_calls(calls), "remove": []}
        return self.make_request('post', '/main/call-log/change-sync/', body)

    def remove_calls_from_log(self, calls: List[dict]) -> dict:
        """
        Remove calls from your calls log.

        :param calls: List of dicts with calls data.
        :type calls: List[dict]
        :return: dict with upload result.
        :rtype: dict

        Example of list of calls to remove::

            [
                {
                    "called_at": "2021-07-29T11:27:50Z",
                    "duration": 28,
                    "name": "043437535",
                    "phone_number": 43437535,
                    "tag": None,
                    "type": "missed",
                },
                {
                    "called_at": "2021-08-08T19:42:59Z",
                    "duration": 0,
                    "name": "Chandler",
                    "phone_number": 334324324,
                    "tag": None,
                    "type": "outgoing",
                },
                {
                    "called_at": "2022-01-03T16:50:24Z",
                    "duration": 15,
                    "name": "Joey",
                    "phone_number": 51495043537,
                    "tag": None,
                    "type": "incoming",
                },
            ]
        """
        body = {"add": [], "remove": validate_calls(calls)}
        return self.make_request('post', '/main/call-log/change-sync/', body)

    def block_profile(self, phone_number: Union[str, int], block_contact=True, me_full_block=True) -> bool:
        """
        Block user profile.

        :param phone_number: User phone number in international format.
        :type phone_number: Union[str, int]
        :param block_contact: To block for calls. Default: ``True``.
        :type block_contact: bool
        :param me_full_block: To block for social. Default: ``True``.
        :type me_full_block: bool
        :return: Is blocking success.
        :rtype: bool
        """
        body = {"block_contact": block_contact, "me_full_block": me_full_block,
                "phone_number": str(self.valid_phone_number(phone_number))}
        return self.make_request('post', '/main/users/profile/block/', body)['success']

    def unblock_profile(self, phone_number: int, block_contact=False, me_full_block=False) -> bool:
        """
        Unblock user profile.

        :param phone_number: User phone number in international format.
        :type phone_number: Union[str, int]
        :param block_contact: To unblock for calls. Default: ``True``.
        :type block_contact: bool
        :param me_full_block: To unblock for social. Default: ``True``.
        :type me_full_block: bool
        :return: Is unblocking success.
        :rtype: bool
        """
        body = {"block_contact": block_contact, "me_full_block": me_full_block,
                "phone_number": str(self.valid_phone_number(phone_number))}
        return self.make_request('post', '/main/users/profile/block/', body)['success']

    def block_numbers(self, numbers: Union[int, List[int]]) -> bool:
        """
        Block numbers.

        :param numbers: Single or list of phone numbers in international format.
        :type numbers: Union[int, List[int]])
        :return: Is blocking success.
        :rtype: bool

        Example::

            [
                {
                    "block_contact": True,
                    "me_full_block": False,
                    "phone_number": 1234567890
                }
            ]
        """
        if not isinstance(numbers, list):
            numbers = [numbers]
        body = {"phone_numbers": numbers}
        return self.make_request('post', '/main/users/profile/bulk-block/', body)['block_contact']

    def unblock_numbers(self, numbers: Union[int, List[int]]) -> bool:
        """
        Unblock numbers.

        :param numbers: Single or list of phone numbers in international format. See :py:func:`get_blocked_numbers`.
        :type numbers: Union[int, List[int]])
        :return: Is unblocking success.
        :rtype: bool
        """
        if not isinstance(numbers, list):
            numbers = [numbers]
        body = {"phone_numbers": numbers}
        return self.make_request('post', '/main/users/profile/bulk-unblock/', body)['success']

    def get_blocked_numbers(self) -> List[dict]:
        """
        Get list of your blocked numbers. See :py:func:`unblock_numbers`.

        :return: list of dicts.
        :rtype: List[dict]

        Example::

            [
                {
                    "block_contact": True,
                    "me_full_block": False,
                    "phone_number": 1234567890
                }
            ]
        """
        return self.make_request('get', '/main/settings/blocked-phone-numbers/')

    def update_location(self, lat: float, lon: float) -> bool:
        """
        Update your location. See :py:func:`upload_random_data`.

        :param lat: location latitude coordinates.
        :type lat: float
        :param lon: location longitude coordinates.
        :type lon: float
        :return: Is location update success.
        :rtype: bool
        """
        if not isinstance(lat, float) or not isinstance(lon, float):
            raise Exception("Not a valid coordination!")
        body = {"location_latitude": float(lat), "location_longitude": float(lon)}
        return self.make_request('post', '/main/location/update/', body)['success']

    def share_location(self, uuid: str) -> bool:
        """
        Share your :py:func:`update_location` with another user.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: is sharing success.
        :rtype: bool
        """
        return self.make_request('post', '/main/users/profile/share-location/' + str(uuid) + "/")['success']

    def get_distance(self, uuid: str) -> Union[float, None]:
        """
        Get your distance between you and another user.
         - Only if the user shared his location with you. you can ask his location with :py:func:`suggest_turn_on_location`.

        :param uuid: User uuid. See :py:func:`get_uuid`.
        :type uuid: str
        :return: The distance between you in kilometers. None if the user not shared his location with you.
        :rtype: Union[float, None]
        """
        results = self.get_profile_info(uuid)
        if results['profile'].get('distance'):
            return results['profile']['distance']
        return None

    def stop_sharing_location(self, uuids: Union[str, List[str]]) -> bool:
        """
        Stop sharing your :py:func:`update_location` with users.

        :param uuids: Single or list of uuids that you want to stop them from watching you location. See :py:func:`locations_shared_by_me`.
        :type uuids: Union[str, List[str]]
        :return: is stopping success.
        :rtype: bool
        """
        if not isinstance(uuids, list):
            uuids = [uuids]
        body = {"uuids": uuids}
        return self.make_request('post', '/main/users/profile/share-location/stop-for-me/', body)['success']

    def stop_shared_location(self, uuids: Union[str, List[str]]) -> bool:
        """
        Stop locations that shared with you.

        :param uuids: Single or list of uuids that you want to stop their location. See :py:func:`locations_shared_with_me`.
        :type uuids: Union[str, List[str]]
        :return: is stopping success.
        :rtype: bool
        """
        if not isinstance(uuids, list):
            uuids = [uuids]
        body = {"uuids": uuids}
        return self.make_request('post', '/main/users/profile/share-location/stop/', body)['success']

    def locations_shared_by_me(self) -> List[dict]:
        """
        Get list of users that you shared your location with them. See also :py:func:`locations_shared_with_me`.

        :return: list of dicts with contacts details.
        :rtype: List[dict]

        Example::

            [
                {
                    "first_name": "Rachel Green",
                    "last_name": "",
                    "phone_number": 1234567890,
                    "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/59XXXXXXXXXfa67.jpg",
                    "uuid": "XXXXX-XXXXX-XXXX-XXXX-XXXXXX"
                }
            ]
        """
        return self.make_request('get', '/main/users/profile/share-location/')

    def locations_shared_with_me(self) -> dict:
        """
        Get users who have shared a location with you. See also :py:func:`locations_shared_by_me`.

        :return: dict with list of uuids and list with users.
        :rtype: dict

        Example::

            {
                "shared_location_user_uuids": [
                    "3850XXX-XXX-XXX-XXX-XXXXX"
                ],
                "shared_location_users": [
                    {
                        "author": {
                            "first_name": "Gunther",
                            "last_name": "",
                            "phone_number": 3647632874324,
                            "profile_picture": "https://d18zaexen4dp1s.cloudfront.net/dXXXXXXXXXXXXXXXXXXb.jpg",
                            "uuid": "3850XXX-XXX-XXX-XXX-XXXXX"
                        },
                        "distance": 1.4099551982832228,
                        "i_shared": False
                    }
                ]
            }
        """

    def upload_random_data(self, contacts=True, calls=True, location=True):
        """
        Upload random data to your account.

        :param contacts: To upload random contacts data. Default: ``True``.
        :type contacts: bool
        :param calls: To upload random calls data. Default: ``True``.
        :type calls: bool
        :param location: To upload random location data. Default: ``True``.
        :type location: bool
        :return: Is uploading success.
        :rtype: bool
        """
        random_data = get_random_data(contacts, calls, location)
        if contacts:
            self.add_contacts(random_data['contacts'])
        if calls:
            self.add_calls_to_log(random_data['calls'])
        if location:
            self.update_location(random_data['location']['lat'], random_data['location']['lon'])
