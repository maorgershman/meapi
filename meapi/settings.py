from typing import Tuple, List
from meapi.exceptions import MeException


class Settings:
    def get_settings(self):
        """
        Get current settings.

        :return: Dict with settings.
        :rtype: dict

        Example::

            {
                "birthday_notification_enabled": True,
                "comments_enabled": True,
                "comments_notification_enabled": True,
                "contact_suspended": False,
                "distance_notification_enabled": True,
                "language": "iw",
                "last_backup_at": None,
                "last_restore_at": None,
                "location_enabled": True,
                "mutual_contacts_available": True,
                "names_notification_enabled": True,
                "notifications_enabled": True,
                "spammers_count": 24615,
                "system_notification_enabled": True,
                "who_deleted_enabled": True,
                "who_deleted_notification_enabled": True,
                "who_watched_enabled": True,
                "who_watched_notification_enabled": True,
            }
        """
        return self.make_request('get', '/main/settings/')

    def change_social_settings(self,
                               mutual_contacts_available: bool = None,
                               who_watched_enabled: bool = None,
                               who_deleted_enabled: bool = None,
                               comments_enabled: bool = None,
                               location_enabled: bool = None,
                               language: str = None) -> Tuple[bool, List[str]]:
        """
        Change social settings.

        :param mutual_contacts_available: Show common contacts between users. Default: None
        :type mutual_contacts_available: bool
        :param who_watched_enabled: Users will be notified that you have viewed their profile. Default: None
            - They will only be able to get information about you if they are premium users (``is_premium`` = True in :py:func:`get_profile_info`) or, by using this libary....
            - This setting must be True if you want to use :py:func:`who_watched` method.
        :type who_watched_enabled: bool
        :param who_deleted_enabled: Users will be notified that you have deleted them from your contact book. Default: None
            - They will only be able to get information about you if they are premium users (``is_premium`` = True in :py:func:`get_profile_info`) or, by using this libary....
            - This setting must be True if you want to use :py:func:`who_deleted` method.
        :type who_deleted_enabled: bool
        :param comments_enabled: Allow users to publish comment (:py:func:`publish_comment`) in your profile. Default: None
            - Comments will not be posted until you approve them with :py:func:`approve_comment`.
        :type comments_enabled: bool
        :param location_enabled: Allow shared locations. Default: None
        :type location_enabled: bool
        :param language: lang code, iw, en, etc. (For notifications). Default: None
        :type language: bool
        :return: Tuple: is success, list of failed
        :rtype: Tuple[bool, list]
        """
        args = locals()
        del args['self']
        body = {}
        for setting, value in args.items():
            if value is not None:
                body[setting] = value
        if not body:
            raise MeException("You need to change at least one setting!")

        results = self.make_request('patch', '/main/settings/', body)
        failed = []
        for setting in body.keys():
            if results[setting] != body[setting]:
                failed.append(setting)
        return not bool(failed), failed
