Reference
==================


Reference for the Me class.

.. currentmodule:: meapi
.. autoclass:: Me


Search
------
.. automethod:: Me.phone_search
.. automethod:: Me.get_profile_info
.. automethod:: Me.get_uuid

Account
-------

.. automethod:: Me.update_profile_info
.. automethod:: Me.add_contacts
.. automethod:: Me.remove_contacts
.. automethod:: Me.add_calls_to_log
.. automethod:: Me.remove_calls_from_log
.. automethod:: Me.block_profile
.. automethod:: Me.unblock_profile
.. automethod:: Me.block_numbers
.. automethod:: Me.unblock_numbers
.. automethod:: Me.get_blocked_numbers
.. automethod:: Me.update_location
.. automethod:: Me.upload_random_data
.. automethod:: Me.delete_account
.. automethod:: Me.suspend_account

Social
--------
.. automethod:: Me.friendship
.. automethod:: Me.report_spam
.. automethod:: Me.who_deleted
.. automethod:: Me.who_watched
.. automethod:: Me.is_spammer
.. automethod:: Me.get_age

Social network
--------------
.. automethod:: Me.get_socials
.. automethod:: Me.add_social
.. automethod:: Me.remove_social
.. automethod:: Me.switch_social_status

Group names
-----------
.. automethod:: Me.get_groups_names
.. automethod:: Me.delete_name
.. automethod:: Me.get_deleted_names
.. automethod:: Me.restore_name
.. automethod:: Me.ask_group_rename

Comments
--------
.. automethod:: Me.get_comments
.. automethod:: Me.get_comment
.. automethod:: Me.publish_comment
.. automethod:: Me.approve_comment
.. automethod:: Me.delete_comment
.. automethod:: Me.like_comment

Notifications
--------------
.. automethod:: Me.unread_notifications_count
.. automethod:: Me.get_notifications
.. automethod:: Me.read_notification

Settings
---------
.. automethod:: Me.get_settings
.. automethod:: Me.change_social_settings
.. automethod:: Me.change_notification_settings

Exceptions
----------
.. currentmodule:: meapi.exceptions
.. autoclass:: MeApiException
.. autoclass:: MeException
