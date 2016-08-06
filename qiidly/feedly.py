# -*- coding: utf-8 -*-
import json
import re
import requests


def feed_id_from_feed_url(feed_url):
    """feed IDに変換します."""
    return 'feed/{url}'.format(url=feed_url)


def feed_url_from_feed_id(feed_id):
    """feed URLに変換します。"""
    x = re.match(r'feed/(.+)', feed_id)
    return x.group(1) if x else None


def category_id_from_user_id_and_category(user_id, category):
    """カテゴリIDに変換します."""
    return 'user/{user_id}/category/{category}'.format(
        user_id=user_id,
        category=category)


def category_from_category_id(category_id):
    x = re.match(r'^user/.*/category/(.+)$', category_id)
    return x.group(1) if x else None


class FeedlyClient:
    """Feedly."""

    def __init__(self, access_token, base_url='https://cloud.feedly.com'):
        self.access_token = access_token
        self.base_url = base_url

    def _headers(self):
        return {
            'content-type': 'application/json',
            'Authorization': 'OAuth ' + self.access_token
        }

    def get_user_profile(self):
        """
        Get the profile of the user.

        https://developer.feedly.com/v3/profile/#get-the-profile-of-the-user
        GET /v3/profile
        (Authorization is required)
        """
        res = requests.get(
            url=self.base_url + '/v3/profile',
            headers=self._headers())
        return res.json()

    def subscribe_feed(self, feed_id, category_id):
        """
        Subscribe to a feed.

        https://developer.feedly.com/v3/subscriptions/#subscribe-to-a-feed

        POST /v3/subscriptions
        (Authorization is required)
        """
        params = {
            'id': feed_id,
            'categories': [{'id': category_id}]
        }
        res = requests.post(url=self.base_url + '/v3/subscriptions',
                            data=json.dumps(params),
                            headers=self._headers())
        return res

    def unsubscribe_feeds(self, feed_ids):
        """
        Unsubscribe from multiple feeds.

        DELETE /v3/subscriptions/.mdelete
        (Authorization is required)
        """
        res = requests.delete(
            url=self.base_url + '/v3/subscriptions/.mdelete',
            data=json.dumps(feed_ids),
            headers=self._headers())
        return res

    def update_feeds(self, subscriptions):
        """
        Update multiple subscriptions.

        https://developer.feedly.com/v3/subscriptions/#update-multiple-subscriptions
        POST /v3/subscriptions/.mput
        (Authorization is required)
        """
        res = requests.post(
            url=self.base_url + '/v3/subscriptions/.mput',
            data=json.dumps(subscriptions),
            headers=self._headers())
        return res

    def get_user_subscriptions(self):
        """
        Get the user’s subscriptions.

        https://developer.feedly.com/v3/subscriptions/#get-the-users-subscriptions
        GET /v3/subscriptions
        (Authorization is required)
        """
        res = requests.get(
            url=self.base_url + '/v3/subscriptions',
            headers=self._headers())
        return res.json()
