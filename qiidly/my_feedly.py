# -*- coding: utf-8 -*-
import json
import requests


def _headers(access_token):
    return {
        'content-type': 'application/json',
        'Authorization': 'OAuth ' + access_token
    }


def to_feed_id(feed_url):
    """feed IDに変換します."""
    return 'feed/{url}'.format(url=feed_url)


def to_category_id(user_id, category):
    """カテゴリIDに変換します."""
    return 'user/{user_id}/category/{category}'.format(
        user_id=user_id,
        category=category)


def get_user_profile(access_token):
    """
    Get the profile of the user.

    https://developer.feedly.com/v3/profile/#get-the-profile-of-the-user
    GET /v3/profile
    (Authorization is required)
    """
    res = requests.get(
        url='https://cloud.feedly.com/v3/profile',
        headers=_headers(access_token))
    return res.json()


def subscribe_feed(access_token, feed_id, category_id):
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
    res = requests.post(url='https://cloud.feedly.com/v3/subscriptions',
                        data=json.dumps(params),
                        headers=_headers(access_token))
    return res


def unsubscribe_feeds(access_token, feed_ids):
    """
    Unsubscribe from multiple feeds.

    DELETE /v3/subscriptions/.mdelete
    (Authorization is required)
    """
    res = requests.delete(
        url='https://cloud.feedly.com/v3/subscriptions/.mdelete',
        data=json.dumps(feed_ids),
        headers=_headers(access_token))
    return res


def update_feeds(access_token, subscriptions):
    """
    Update multiple subscriptions.

    https://developer.feedly.com/v3/subscriptions/#update-multiple-subscriptions
    POST /v3/subscriptions/.mput
    (Authorization is required)
    """
    res = requests.post(
        url='https://cloud.feedly.com/v3/subscriptions/.mput',
        data=json.dumps(subscriptions),
        headers=_headers(access_token))
    return res


def get_user_subscriptions(access_token):
    """
    Get the user’s subscriptions.

    https://developer.feedly.com/v3/subscriptions/#get-the-users-subscriptions
    GET /v3/subscriptions
    (Authorization is required)
    """
    res = requests.get(
        url='https://cloud.feedly.com/v3/subscriptions',
        headers=_headers(access_token))
    return res.json()
