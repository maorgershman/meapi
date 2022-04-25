from typing import Tuple, List, Union
from meapi.exceptions import MeException

notification_categories = {
    'names': ['JOINED_ME', 'CONTACT_ADD', 'UPDATED_CONTACT', 'DELETED_CONTACT', 'NEW_NAME_REQUEST',
              'NEW_NAME_REQUEST_APPROVED'],
    'system': ['NAME_SUGGESTION_UPDATED', 'SPAM_SUGGESTION_APPROVED', 'TURN_ON_MUTUAL', 'NONE'],
    'comments': ['NEW_COMMENT', 'PUBLISHED_COMMENT', 'TURN_ON_COMMENTS'],
    'who_watch': ['WEEKLY_VISITS'],
    'birthday': ['BIRTHDAY'],
    'location': ['TURN_ON_LOCATION', 'SHARE_LOCATION'],
    'who_deleted': ['WEEKLY_DELETED']
}


class Notifications:
    def unread_notifications_count(self) -> int:
        """
        Get count of unread notifications.

        :return: count of notifications.
        :rtype: int
        """
        return self.make_request('get', '/notification/notification/count/')['count']

    def get_notifications(self,
                          page_number: int = 1,
                          results_limit: int = 20,
                          names_filter: bool = False,
                          system_filter: bool = False,
                          comments_filter: bool = False,
                          who_watch_filter: bool = False,
                          who_deleted_filter: bool = False,
                          birthday_filter: bool = False,
                          location_filter: bool = False) -> dict:
        """
        Get app notifications: new names, birthdays, comments, watches, deletes, location shares and system notifications.

        :param page_number: :py:func:`get_notifications_uuid` [``'count'``] / ``page_size`` = ``pages``. Default: 1
        :type page_number: int
        :param results_limit: Limit of notifications in each page. Default: 20
        :type results_limit: int
        :param names_filter: New names, deletes, joined, renames, rename requests. Default: False
        :type names_filter: bool
        :param system_filter: System notifications: spam reports, your name requests, suggestions to turn on mutual contacts. Default: False
        :type system_filter: bool
        :param comments_filter: Comments notifications: new comments, published comments and suggestions to turn on comments (See :py:func:`get_comments`). Default: False
        :type comments_filter: bool
        :param who_watch_filter: Who watched your profile (See :py:func:`who_watched`). Default: False
        :type who_watch_filter: bool
        :param who_deleted_filter: Who deleted you from his contacts (See :py:func:`who_deleted`). Default: False
        :type who_deleted_filter: bool
        :param birthday_filter: Contacts birthdays (See :py:func:`get_age`). Default: False
        :type birthday_filter: bool
        :param location_filter: Shared locations: suggestions to turn on location, locations that shared with you. Default: False
        :type location_filter: bool
        :return: Dict with notifications
        :rtype: dict

        Example::

            {
                "count": 94,
                "next": "https://app.mobile.me.app/notification/notification/items/?page=2&page_size=30&status=distributed",
                "previous": None,
                "results": [
                    {
                        "id": 103466332,
                        "created_at": "2022-03-18T11:17:09Z",
                        "modified_at": "2022-03-18T11:17:09Z",
                        "is_read": False,
                        "sender": "2e7XXX-84XXXX-4ec7-b6cb-d4XXXXXX",
                        "status": "distributed",
                        "delivery_method": "push",
                        "distribution_date": "2022-03-18T11:17:09Z",
                        "message_subject": None,
                        "message_category": "BIRTHDAY",
                        "message_body": None,
                        "message_lang": "iw",
                        "context": {
                            "name": "Ross geller",
                            "uuid": "2e7XXXX-XXXX-XXXX-b6cXb-d46XXXXX1",
                            "category": "BIRTHDAY",
                            "phone_number": 97849743536,
                            "notification_id": None,
                            "profile_picture": None,
                        },
                    },
                    {
                        "id": 18987495325,
                        "created_at": "2022-04-06T11:18:03Z",
                        "modified_at": "2022-04-06T11:18:03Z",
                        "is_read": False,
                        "sender": "5XXXXX0e-XXXX-XXXX-XXXX-XXXXXXX",
                        "status": "distributed",
                        "delivery_method": "push",
                        "distribution_date": "2022-04-06T11:18:03Z",
                        "message_subject": None,
                        "message_category": "UPDATED_CONTACT",
                        "message_body": None,
                        "message_lang": "iw",
                        "context": {
                            "name": "Chandler",
                            "uuid": "XXXXXX-XXXX-XXXXX-XXX-XXXXX",
                            "category": "UPDATED_CONTACT",
                            "new_name": "Your new name",
                            "phone_number": 8479843759435,
                            "notification_id": None,
                            "profile_picture": None,
                        },
                    },
                    {
                        "id": 17983743351,
                        "created_at": "2022-04-11T06:45:27Z",
                        "modified_at": "2022-04-11T06:45:27Z",
                        "is_read": False,
                        "sender": "XXXXXX-XXXX-XXXXX-XXX-XXXXX",
                        "status": "distributed",
                        "delivery_method": "push",
                        "distribution_date": "2022-04-11T06:45:27Z",
                        "message_subject": None,
                        "message_category": "CONTACT_ADD",
                        "message_body": None,
                        "message_lang": "iw",
                        "context": {
                            "name": "Monica",
                            "uuid": "XXXXXX-XXXX-XXXXX-XXX-XXXXX",
                            "category": "CONTACT_ADD",
                            "new_name": "Ross",
                            "phone_number": 878634535436,
                            "notification_id": None,
                            "profile_picture": None,
                        },
                    },
                ],
            }
        """
        args = locals()
        del args['self']
        filters = []
        for fil, val in args.items():
            if val:
                filters = [*filters, *notification_categories[fil.replace("_filter", "")]]
        params = f"?page={page_number}&page_size={results_limit}&status=distributed"
        if filters:
            params += f"&categories=%5B{'%2C%20'.join(filters)}%5D"
        return self.make_request('get', '/notification/notification/items/' + params)

    def read_notification(self, notification_id: Union[int, str]) -> bool:
        """
        Mark notification as read.

        :param notification_id: Notification id from :py:func:`get_notifications`.
        :type notification_id: Union[int, str]
        :return: Is read success.
        :rtype: bool
        """
        body = {"notification_id": int(notification_id)}
        return self.make_request('post', '/notification/notification/read/', body)['is_read']

    def change_notification_settings(self,
                                     who_deleted_notification_enabled: bool = None,
                                     who_watched_notification_enabled: bool = None,
                                     distance_notification_enabled: bool = None,
                                     system_notification_enabled: bool = None,
                                     birthday_notification_enabled: bool = None,
                                     comments_notification_enabled: bool = None,
                                     names_notification_enabled: bool = None,
                                     notifications_enabled: bool = None) -> Tuple[bool, List[str]]:
        """
        Set new settings for notifications.

        :param who_deleted_notification_enabled: Default: None
        :type who_deleted_notification_enabled: bool
        :param who_watched_notification_enabled: Default: None
        :type who_watched_notification_enabled: bool
        :param distance_notification_enabled: Default: None
        :type distance_notification_enabled: bool
        :param system_notification_enabled: Default: None
        :type system_notification_enabled: bool
        :param birthday_notification_enabled: Default: None
        :type birthday_notification_enabled: bool
        :param comments_notification_enabled: Default: None
        :type comments_notification_enabled: bool
        :param names_notification_enabled: Default: None
        :type names_notification_enabled: bool
        :param notifications_enabled: Default: None
        :type notifications_enabled: bool
        :return: Tuple of: is success, list of failed
        :rtype: Tuple[bool, list]
        """
        args = locals()
        del args['self']
        body = {}
        for setting, value in args.items():
            if value is not None:
                body[setting] = value
        if not body:
            raise MeException("You need to provide at least one setting!")

        results = self.make_request('patch', '/main/settings/', body)
        failed = []
        for setting in body.keys():
            if results[setting] != body[setting]:
                failed.append(setting)
        return not bool(failed), failed
