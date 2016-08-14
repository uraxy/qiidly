# -*- coding: utf-8 -*-
import re
from qiita_v2.client import QiitaClient


def tag_feed_url_from_tag_id(tag_id):
    return 'http://qiita.com/tags/{tag}/feed.atom'.format(tag=tag_id)


def tag_id_from_tag_feed_url(tag_feed_url):
    x = re.match(r'http://qiita.com/tags/(.+)/feed.atom', tag_feed_url)
    return x.group(1) if x else None


def user_feed_url_from_user_id(user_id):
    return 'http://qiita.com/{user_id}/feed.atom'.format(user_id=user_id)


def user_id_from_user_feed_url(user_feed_url):
    x = re.match(r'http://qiita.com/(.+)/feed.atom', user_feed_url)
    return x.group(1) if x else None


class MyQiitaClient:
    """My Qiita Client."""

    def __init__(self, access_token):
        self.access_token = access_token
        self.qiita_client = QiitaClient(access_token=access_token)

    def _get_all_pages(self, func, user_id):
        """ページ分けされたレスポンスを巡回してすべてのアイテムを取得します."""
        QIITA_ITEMS_PER_PAGE = 100
        QIITA_MAX_PAGE = 100
        results = []

        for i in range(1, QIITA_MAX_PAGE + 1):
            res = func(
                user_id,
                params={'page': i, 'per_page': QIITA_ITEMS_PER_PAGE})
            t = res.to_json()
            results.extend(t)
            if len(t) < QIITA_ITEMS_PER_PAGE:  # last page
                break
        return results

    def get_following_tags(self, user_id):
        """
        ユーザがフォローしているタグ一覧をフォロー日時の降順で返します.

        GET /api/v2/users/:user_id/following_tags
        https://qiita.com/api/v2/docs#get-apiv2usersuser_idfollowing_tags
        """
        func = self.qiita_client.list_user_following_tags
        return self._get_all_pages(func, user_id)

    def get_followees(self, user_id):
        """
        ユーザがフォローしているユーザ一覧を取得します.

        GET /api/v2/users/:user_id/followees
        https://qiita.com/api/v2/docs#get-apiv2usersuser_idfollowees
        """
        func = self.qiita_client.list_user_followees
        return self._get_all_pages(func, user_id)

    def get_user_id(self):
        """
        Qiitaのuser_idを返します.

        アクセストークンに紐付いたユーザを返します。
        GET /api/v2/authenticated_user
        https://qiita.com/api/v2/docs#get-apiv2authenticated_user
        """
        res = self.qiita_client.get_authenticated_user()
        user_id = (res.to_json())['id']
        return user_id

    def get_following_tag_feed_urls(self, user_id):
        """Qiitaでフォローしているタグに対応するfeed urlのリストを返します."""
        tags = self.get_following_tags(user_id)
        tag_feed_urls = [tag_feed_url_from_tag_id(tag['id']) for tag in tags]
        return tag_feed_urls

    def get_followees_feed_urls(self, user_id):
        """Qiitaでフォローしているユーザーに対応するfeed urlのリストを返します."""
        followees = self.get_followees(user_id)
        user_feed_urls = [user_feed_url_from_user_id(followee['id']) for followee in followees]
        return user_feed_urls
