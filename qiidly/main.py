# -*- coding: utf-8 -*-
"""dummy docstring."""
import copy
from . import qiita
from . import feedly


FEEDLY_CATEGORY_TAGS = 'Qiita:tags'
FEEDLY_CATEGORY_FOLLOWEES = 'Qiita:followees'


def tag_id_from_feed_id(feed_id):
    """Feedlyのfeed_idからQiitaのtag_idを抽出します."""
    feed_url = feedly.feed_url_from_feed_id(feed_id)
    tag_id = qiita.tag_id_from_tag_feed_url(feed_url)
    return tag_id


def user_id_from_feed_id(feed_id):
    """Feedlyのfeed_idからQiitaのuser_idを抽出します."""
    feed_url = feedly.feed_url_from_feed_id(feed_id)
    user_id = qiita.user_id_from_user_feed_url(feed_url)
    return user_id


class Qiidly:
    """Qiidly."""

    # $ python qiidly/qiidly.py -q $QIITA_TOKEN -f $FEEDLY_TOKEN
    #
    # Qiita APIのアクセストークン
    # 「設定 > 共通:アプリケーション > 個人用アクセストークン」から発行する。

    # Feedly Cloud APIのアクセストークン
    # How do I generate a developer access token?
    # https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token

    # Feedlyで購読するときに付けるCategory

    def __init__(self, qiita_token, feedly_token, target='tags'):
        """dummy.

        ネットワークアクセスなし
        :param target: Syncする対象。'tags' or 'followees'
        :type target: str
        """
        self.target = target
        if target == 'tags':
            self.feedly_category = FEEDLY_CATEGORY_TAGS
        elif target == 'followees':
            self.feedly_category = FEEDLY_CATEGORY_FOLLOWEES
        else:
            raise ValueError("Invalid target. Must be one of ['tags', 'followees']: '{target}'".format(target=target))

        self.qiita_client = qiita.MyQiitaClient(qiita_token)
        self.feedly_client = feedly.FeedlyClient(feedly_token)

        self.todo_checked = False

    def _check_todo(self):
        """ネットワークアクセスあり."""
        feedly_user_profile = self.feedly_client.get_user_profile()
        feedly_user_id = feedly_user_profile['id']

        self.qiidly_category_id = feedly.category_id_from_user_id_and_category(feedly_user_id, self.feedly_category)

        if self.target == 'tags':
            self.qiita_feed_ids = self._get_qiita_tag_feed_ids()
        elif self.target == 'followees':
            self.qiita_feed_ids = self._get_qiita_followee_feed_ids()
        else:
            self.qiita_feed_ids = None

        self.feedly_subscriptions = self._get_feedly_subscriptions()
        self.todo = self._build_todo()

        self.todo_checked = True

    def _build_todo(self):
        """ネットワークアクセスなし."""
        # 1. Qiitaでfollowしているものについて
        # 1-1. Feedlyで購読あり
        #      -> FEEDLY_CATEGORYがなければ、カテゴリに追加し更新対象へ
        #         FEEDLY_CATEGORYがあれば、なにもしない
        # 1-2. Feedlyで購読なし -> 購読追加対象へ
        #
        # 2. Feedlyで購読しているものについて
        # 2-1. Qiitaでフォローしている -> skip (1-2で処理済み）
        # 2-2. Qiitaでフォローしていない
        #      -> カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
        #         0個の場合は購読削除対象へ
        #         1個以上の場合は更新対象へ
        # 3. Feedlyに購読追加対象、購読削除対象、購読更新対象を反映
        # 新たにFeedlyで購読する必要のあるfeed URLのリスト
        todo = {
            'subscribe_ids': [],
            'add_categories': [],
            'remove_categories': [],
            'unsubscribe_ids': [],
        }
        for q in self.qiita_feed_ids:  # 1. Qiitaでfollowしているものについて
            for f_sub in self.feedly_subscriptions:
                if f_sub['id'] == q:  # 1-1. Feedlyで購読あり
                    # カテゴリIDを取り出します
                    f_categ_ids = [s['id'] for s in f_sub['categories']]
                    if self.qiidly_category_id not in f_categ_ids:
                        # FEEDLY_CATEGORYがなければ、カテゴリに追加し更新対象へ
                        s = {'title': f_sub['title'],
                             'id': f_sub['id'],
                             'categories': copy.deepcopy(f_sub['categories'])}
                        s['categories'].append({'id': self.qiidly_category_id})
                        todo['add_categories'].append(s)
                    else:  # FEEDLY_CATEGORYがあれば、何もしなくて良い
                        pass
                    break
            else:  # 1-2. Feedlyで購読なし -> 購読追加対象へ
                todo['subscribe_ids'].append(q)

        # 2. Feedlyで購読しているものについて
        # 2-1. Qiitaでフォローしている -> skip (1-2で処理済み）
        # 2-2. Qiitaでフォローしていない
        #      -> カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
        #         0個の場合は購読削除対象へ
        #         1個以上の場合は更新対象へ
        for f_sub in self.feedly_subscriptions:
            # 2-1. Qiitaでフォローしている -> skip (1-2で処理済み）
            if f_sub['id'] in self.qiita_feed_ids:
                continue
            # 2-2. Qiitaでフォローしていない
            #      -> カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
            #         0個の場合は購読削除対象へ
            #         1個以上の場合は更新対象へ

            # カテゴリIDを取り出します
            f_categ_ids = [s['id'] for s in f_sub['categories']]
            # Qiita用のFEEDLY_CATEGORYがついていない、無関係の購読はskip
            if self.qiidly_category_id not in f_categ_ids:
                continue
            # カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
            # 0個の場合は購読削除対象へ
            if len(f_categ_ids) <= 1:
                todo['unsubscribe_ids'].append(f_sub['id'])
                continue
            # 1個以上の場合は更新対象へ
            new_categs = [x for x in f_sub['categories'] if x['id'] != self.qiidly_category_id]
            s = {'title': f_sub['title'],
                 'id': f_sub['id'],
                 'categories': new_categs}
            todo['remove_categories'].append(s)

        return todo

    def have_to_sync(self):
        """
        QiitaとFeedlyがsync済みかどうかチェックします.

        未チェックの場合は、ネットワークアクセスあり.
        :returns: Syncする必要があるか？
        :rtype: bool
        """
        if not self.todo_checked:
            self._check_todo()
        return (self.todo['subscribe_ids'] or
                self.todo['add_categories'] or
                self.todo['remove_categories'] or
                self.todo['unsubscribe_ids'])

    def print_todo(self):
        """dummy."""
        if self.target == 'tags':
            id_from_feed_id = tag_id_from_feed_id
        elif self.target == 'followees':
            id_from_feed_id = user_id_from_feed_id
        else:
            id_from_feed_id = None

        print("## Category at Qiita: '{}'".format(self.feedly_category))

        for x in self.todo['subscribe_ids']:
            qiita_id = id_from_feed_id(x)
            print('+ {}'.format(qiita_id))

        for x in self.todo['unsubscribe_ids']:
            qiita_id = id_from_feed_id(x)
            print('- {}'.format(qiita_id))

        for x in self.todo['add_categories']:
            new_categs = [feedly.category_from_category_id(c['id']) for c in x['categories']]
            print('+ {}\t=> categories{}'.format(id_from_feed_id(x['id']),
                                                 new_categs))

        for x in self.todo['remove_categories']:
            new_categs = [feedly.category_from_category_id(c['id']) for c in x['categories']]
            print('- {}\t=> categories{}'.format(id_from_feed_id(x['id']),
                                                 new_categs))

    def _get_qiita_tag_feed_ids(self):
        """Qiitaでフォローしているタグに対応するfeed_idのリストを返します."""
        uid = self.qiita_client.get_user_id()
        urls = self.qiita_client.get_following_tag_feed_urls(uid)
        qiita_feed_ids = [feedly.feed_id_from_feed_url(x) for x in urls]

        return qiita_feed_ids

    def _get_qiita_followee_feed_ids(self):
        """Qiitaでフォローしているユーザーに対応するfeed_idのリストを返します."""
        uid = self.qiita_client.get_user_id()
        urls = self.qiita_client.get_followees_feed_urls(uid)
        qiita_feed_ids = [feedly.feed_id_from_feed_url(x) for x in urls]

        return qiita_feed_ids

    def _get_feedly_subscriptions(self):
        subscriptions = self.feedly_client.get_user_subscriptions()

        return subscriptions

    def sync(self):
        """
        QiitaでのフォローをFeedlyにSyncします.
        """
        if not self.todo_checked:
            self._check_todo()
        for f in self.todo['subscribe_ids']:
            self.feedly_client.subscribe_feed(f, self.qiidly_category_id)
        if self.todo['unsubscribe_ids']:
            self.feedly_client.unsubscribe_feeds(self.todo['unsubscribe_ids'])
        to_update = self.todo['add_categories'] + self.todo['remove_categories']
        if to_update:
            self.feedly_client.update_feeds(to_update)
