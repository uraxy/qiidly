# -*- coding: utf-8 -*-
from qiita_v2.client import QiitaClient


def _to_tag_feed_url(tag):
    return 'http://qiita.com/tags/{tag}/feed.atom'.format(tag=tag['id'])


class MyQiitaClient:
    """My Qiita Client"""

    def __init__(self, access_token):
        self.access_token = access_token
        self.qiita_client = QiitaClient(access_token=access_token)

    def get_following_tags(self, user_id):
        QIITA_TAGS_PER_PAGE = 100
        QIITA_MAX_PAGE = 100
        tags = []

        for i in range(1, QIITA_MAX_PAGE + 1):
            # https://qiita.com/api/v2/docs#get-apiv2usersuser_idfollowing_tags
            res = self.qiita_client.list_user_following_tags(
                user_id,
                params={'page': i, 'per_page': QIITA_TAGS_PER_PAGE})
            t = res.to_json()
            tags.extend(t)
            if len(t) < QIITA_TAGS_PER_PAGE:  # last page
                break
        return tags

    def get_user_id(self):
        # https://qiita.com/api/v2/docs#get-apiv2authenticated_user
        res = self.qiita_client.get_authenticated_user()
        user_id = (res.to_json())['id']

        return user_id

    def get_following_tag_feed_urls(self, user_id):
        tags = self.get_following_tags(user_id)
        tag_feed_urls = [_to_tag_feed_url(tag) for tag in tags]

        return tag_feed_urls
