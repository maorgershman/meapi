from re import match, sub
from typing import List, Union, Tuple
from meapi.exceptions import MeException, MeApiException


class Social:

    def friendship(self, phone_number: int) -> dict:
        """
        Get info like count mutual friends, total calls duration, how do you name each other,
         calls count, your watches, comments, and more.
        :param phone_number: phone number of the person
        :return: dict with friendship data
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-friendship-py
        """
        return self.make_request('get', '/main/contacts/friendship/?phone_number=' + str(self.valid_phone_number(phone_number)))

    def report_spam(self, country_code: str, spam_name: str, phone_number: Union[str, int]) -> bool:
        """
        Report spam on phone number.
        :param country_code: 2 letters code, IL, IT, US etc.
        :param spam_name: the spam name that you want to give to the spammer
        :param phone_number: spammer phone number
        :return: is report success
        """
        body = {"country_code": country_code.upper(), "is_spam": True, "is_from_v": False,
                "name": str(spam_name), "phone_number": str(self.valid_phone_number(phone_number))}
        return self.make_request('post', '/main/names/suggestion/report/', body)['success']

    def who_deleted(self) -> List[dict]:
        """
        Get list of contacts dicts who deleted you from their contacts.
        ** who_deleted must be enabled in your settings account: me_client.change_social_settings(who_deleted = True) **
        :return: list of dicts
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-who_deleted-py
        """
        return self.make_request('get', '/main/users/profile/who-deleted/')

    def who_watched(self) -> List[dict]:
        """
        Get list of contacts dicts who watched your profile.
        ** who_watched must be enabled in your settings account: me_client.change_social_settings(who_watched = True) **
        :return: list of dicts
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-who_watched-py
        """
        return self.make_request('get', '/main/users/profile/who-watched/')

    def get_comments(self, uuid: str = None) -> dict:
        """
        Get user comments
        :param uuid: if none, get self comments
        :return: dict with list of comments
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-comments-py
        """
        if not uuid:
            uuid = self.uuid
        return self.make_request('get', '/main/comments/list/' + uuid)

    def get_comment(self, comment_id) -> dict:
        """
        Get comment details, who liked, create time and more
        :param comment_id:
        :return: dict of details
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-comment-py
        """
        return self.make_request('get', '/main/comments/retrieve/' + str(comment_id))

    def approve_comment(self, comment_id: int) -> bool:
        """
        Approve user comment
        :param comment_id: comment id
        :return: is approve success
        """
        return bool(self.make_request('post', '/main/comments/approve/' + str(comment_id))['status'] == 'approved')

    def delete_comment(self, comment_id: int) -> bool:
        """
        Ignore user comment
        :param comment_id: comment id
        :return: is delete success
        """
        return bool(self.make_request('delete', '/main/comments/approve/' + str(comment_id))['status'] == 'ignored')

    def like_comment(self, comment_id: int) -> dict:
        """
        Like comment
        :param comment_id: comment id
        :return: is like success
        """
        return self.make_request('post', '/main/comments/like/' + str(comment_id))

    def publish_comment(self, uuid: str, comment: str) -> Union[int, bool]:
        """
        Publish comment for another user
        :param uuid: uuid of the commented user
        :param comment: your comment
        :return: comment id if success, else falsy
        """
        body = {"message": str(comment)}
        results = self.make_request('get', '/main/comments/add/' + str(uuid), body)
        return results.get('id') if results.get('status') == 'waiting' else False

    def get_groups(self) -> dict:
        """
        How people named you
        :return: dict with groups
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-groups-py
        """
        return self.make_request('get', '/main/names/groups/')

    def get_deleted_groups(self) -> dict:
        """
        Get deleted group names
        :return: dict with names and id's
        """
        return self.make_request('get', '/main/settings/hidden-names/')

    def delete_group_name(self, group_ids: Union[int, List[int]]) -> bool:
        """
        Delete group name
        :param group_ids: group ids
        :return:
        """
        if not isinstance(group_ids, list):
            group_ids = [group_ids]
        body = {"contact_ids": [str(_id) for _id in group_ids]}
        return self.make_request('get', '/main/contacts/hide/', body)['success']

    def restore_group(self, group_ids: Union[int, List[int]]) -> bool:
        """
        Restore deleted group from get_deleted_groups()
        :param group_ids: group id/s
        :return: is success
        """
        if not isinstance(group_ids, list):
            group_ids = [group_ids]
        body = {"contact_ids": [int(_id) for _id in group_ids]}
        return self.make_request('post', '/main/settings/hidden-names/', body)['success']

    def ask_group_rename(self, group_id: int, new_name: str) -> bool:
        """
        Suggest new name to group of people
        :param group_id: Group id (contact_ids)
        :param new_name: Suggested name
        :return: is success
        """
        body = {"contact_ids": [group_id], "name": new_name}
        return self.make_request('post', '/main/names/suggestion/', body)['success']

    def get_socials(self, uuid: False) -> dict:
        """
        Get account connected social networks
        :param uuid: if not uuid, return self account socials
        :return: dict with social network and posts
        example: https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-socials-py
        """
        if not uuid:
            return self.make_request('get', '/main/social/update/')
        else:
            return self.extra_info(str(uuid))['social']

    def add_social(self,
                   twitter_token: str = None,
                   spotify_token: str = None,
                   instagram_token: str = None,
                   facebook_token: str = None,
                   pinterest_url: str = None,
                   linkedin_url: str = None, ) -> Tuple[bool, List[str]]:
        """
        Add social network to your me account.
        if you have at least 2 socials, you get is_verified = true in your profile (blue check).
        :param twitter_token: Get token introduction - 'https://gist.github.com/david-lev/b158f1cc0cc783dbb13ff4b54416ceec#file-twitter_token-md'
        :param spotify_token: Get token - 'https://accounts.spotify.com/authorize?client_id=0b1ea72f7dce420583038b49fd04be50&response_type=code&redirect_uri=https://app.mobile.me.app/&scope=user-read-email%20playlist-read-private%27'
        :param instagram_token: Get token - 'https://api.instagram.com/oauth/authorize/?app_id=195953705182737&redirect_uri=https://app.mobile.me.app/&response_type=code&scope=user_profile,user_media%27'
        :param facebook_token: Get token - 'https://m.facebook.com/v12.0/dialog/oauth?cct_prefetching=0&client_id=799397013456724%27'
        :param pinterest_url: Url - 'https://www.pinterest.com/username/'
        :param linkedin_url: Url 'https://www.linkedin.com/in/username'
        :return: (bool is_success, list of failed)
        """
        args = locals()
        if sum(bool(i) for i in args.values()) < 2:  # self also true
            raise MeException("You need to provide at least one social!")
        failed = []
        for social, token_or_url in args.items():
            if token_or_url is not None:
                if 'url' in social:
                    if match(r"^https?:\/\/.*{domain}.*$".format(domain=social.replace('_url', '')), token_or_url):
                        field_name = 'profile_id'
                        endpoint = 'update-url'
                        is_token = False
                    else:
                        raise MeException(f"{social.replace('_url', '').capitalize()} accepted profile url!")
                else:
                    field_name = 'code_first'
                    endpoint = 'save-auth-token'
                    is_token = True
                social_name = sub(r'_(token|url)$', '', social)
                body = {'social_name': social_name, field_name: token_or_url}
                results = self.make_request('post', f'/main/social/{endpoint}/', body)
                if not (bool(results['success']) if is_token else bool(results[social_name]['profile_id'] == token_or_url)):
                    failed.append(social_name)
        return not bool(failed), failed

    def remove_social(self,
                      twitter: bool = False,
                      spotify: bool = False,
                      instagram: bool = False,
                      facebook: bool = False,
                      pinterest: bool = False,
                      linkedin: bool = False,
                      ) -> bool:
        """
        Remove social media from your profile
        :param twitter:
        :param spotify:
        :param instagram:
        :param facebook:
        :param pinterest:
        :param linkedin:
        :return: is removal success
        """
        args = locals()
        true_values = sum(bool(i) for i in args.values())
        if true_values < 2:  # self also true
            raise MeException("You need to remove at least one social!")
        successes = 0
        for social, value in args.items():
            if value and isinstance(value, bool):
                body = {"social_name": str(social)}
                if self.make_request('post', '/main/social/delete/', body).get('success'):
                    successes += 1
        return bool(true_values - 1 == successes)

    def switch_social_status(self,
                             twitter: bool = None,
                             spotify: bool = None,
                             instagram: bool = None,
                             facebook: bool = None,
                             pinterest: bool = None,
                             linkedin: bool = None,
                             ) -> bool:
        """
        Switch social network status: hide or show
        :param twitter:
        :param spotify:
        :param instagram:
        :param facebook:
        :param pinterest:
        :param linkedin:
        :return: is switch success (you get true even if social won't set before)
        """
        args = locals()
        not_null_values = sum(bool(i) for i in args.values() if i is not None)
        if not_null_values < 2:  # self also true
            raise MeException("You need to switch at least one social!")
        successes = 0
        for social, status in args.items():
            if status is not None and isinstance(status, bool):
                body = {"social_name": str(social)}
                try:
                    new_status = bool(not self.make_request('post', '/main/social/hide/', body)['is_hidden'])
                except MeApiException as err:
                    if err.status_http == 400 and err.msg['detail'] == 'api_token_does_not_exists':
                        new_status = status
                    else:
                        raise err
                if status == new_status:
                    successes += 1

        return bool(not_null_values == successes)

    def numbers_count(self):
        """
        Get total count of numbers on Me
        :return: total count
        """
        return self.make_request('get', '/main/contacts/count/')['count']

    def suggest_turn_on_comments(self, uuid: str) -> bool:
        """
        Ask user to turn on comments in his account
        :param uuid: user uuid
        :return: is request success
        """
        body = {"uuid": str(uuid)}
        return self.make_request('post', '/main/users/profile/suggest-turn-on-comments/', body)['requested']

    def suggest_turn_on_mutual(self, uuid: str) -> bool:
        """
        Ask user to turn on mutual contacts
        :param uuid: user uuid
        :return: is request success
        """
        body = {"uuid": str(uuid)}
        return self.make_request('post', '/main/users/profile/suggest-turn-on-mutual/', body)['requested']
