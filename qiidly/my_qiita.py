# -*- coding: utf-8 -*-
from qiita_v2.client import QiitaClient


def get_following_tags(access_token, user_id):
    client = QiitaClient(access_token=access_token)

    QIITA_TAGS_PER_PAGE = 100
    QIITA_MAX_PAGE = 100
    tags = []

    for i in range(1, QIITA_MAX_PAGE + 1):
        # https://qiita.com/api/v2/docs#get-apiv2usersuser_idfollowing_tags
        res = client.list_user_following_tags(
            user_id,
            params={'page': i, 'per_page': QIITA_TAGS_PER_PAGE})
        t = res.to_json()
        tags.extend(t)
        if len(t) < QIITA_TAGS_PER_PAGE:  # last page
            break
    return tags


def get_user_id(access_token):
    client = QiitaClient(access_token=access_token)
    # https://qiita.com/api/v2/docs#get-apiv2authenticated_user
    res = client.get_authenticated_user()
    user_id = (res.to_json())['id']

    return user_id


def to_tag_feed_url(tag):
    return 'http://qiita.com/tags/{tag}/feed.atom'.format(tag=tag['id'])


def get_following_tag_feed_urls(access_token, user_id):
    # user_id = get_user_id(access_token)
    tags = get_following_tags(access_token, user_id)
    tag_feed_urls = [to_tag_feed_url(tag) for tag in tags]

    return tag_feed_urls
