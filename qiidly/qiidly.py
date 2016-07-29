# -*- coding: utf-8 -*-
"""dummy docstring."""
import copy
import argparse
import qiita
import feedly


# $ python qiidly/qiidly.py -q $QIITA_TOKEN -f $FEEDLY_TOKEN
#
# Qiita APIのアクセストークン
# 「設定 > 共通:アプリケーション > 個人用アクセストークン」から発行する。

# Feedly Cloud APIのアクセストークン
# How do I generate a developer access token?
# https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token

# Feedlyで購読するときに付けるCategory
FEEDLY_CATEGORY = 'Qiita:tags'


# http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def _query_yes_no(question, default=None):
    valid = {'yes': True, 'y': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == "yes":
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError("invalid default answer: '{default}'".format(default=default))

    while True:
        print(question + prompt, end='')
        choice = input().lower()
        if choice == '' and default is not None:
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'y' or 'n'.")


def _arg_parser():
    parser = argparse.ArgumentParser(description='qiidly: Qiita to Feedly.')
    parser.add_argument('-q', '--qiita-token',
                        required=True,
                        help='Qiita access token')
    parser.add_argument('-f', '--feedly-token',
                        required=True,
                        help='Feedly developer access token')
    return parser


def _create_todo(qiita_feed_ids, subscriptions):
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
    for q in qiita_feed_ids:  # 1. Qiitaでfollowしているものについて
        for f_sub in subscriptions:
            if f_sub['id'] == q:  # 1-1. Feedlyで購読あり
                # カテゴリIDを取り出します
                f_categ_ids = [s['id'] for s in f_sub['categories']]
                if qiidly_category_id not in f_categ_ids:
                    # FEEDLY_CATEGORYがなければ、カテゴリに追加し更新対象へ
                    s = {'title': f_sub['title'],
                         'id': f_sub['id'],
                         'categories': copy.deepcopy(f_sub['categories'])}
                    s['categories'].append({'id': qiidly_category_id})
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
    for f_sub in subscriptions:
        # 2-1. Qiitaでフォローしている -> skip (1-2で処理済み）
        if f_sub['id'] in qiita_feed_ids:
            continue
        # 2-2. Qiitaでフォローしていない
        #      -> カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
        #         0個の場合は購読削除対象へ
        #         1個以上の場合は更新対象へ

        # カテゴリIDを取り出します
        f_categ_ids = [s['id'] for s in f_sub['categories']]
        # Qiita用のFEEDLY_CATEGORYがついていない、無関係の購読はskip
        if qiidly_category_id not in f_categ_ids:
            continue
        # カテゴリからFEEDLY_CATEGORYを除去し、残ったカテゴリが
        # 0個の場合は購読削除対象へ
        if len(f_categ_ids) <= 1:
            todo['unsubscribe_ids'].append(f_sub['id'])
            continue
        # 1個以上の場合は更新対象へ
        new_categs = [x for x in f_sub['categories'] if x['id'] != qiidly_category_id]
        s = {'title': f_sub['title'],
             'id': f_sub['id'],
             'categories': new_categs}
        todo['remove_categories'].append(s)

    return todo


def _up_to_date(todo):
    return not (todo['subscribe_ids'] or
                todo['add_categories'] or
                todo['remove_categories'] or
                todo['unsubscribe_ids'])


def _print_todo(todo):
    print('Sync Feedly with Qiita:')
    print('=======================')

    print()
    print('## feed-IDs to subscribe newly:')
    if todo['subscribe_ids']:
        print(todo['subscribe_ids'])

    print()
    print('## feed-IDs to unsubscribe:')
    if todo['unsubscribe_ids']:
        print(todo['unsubscribe_ids'])

    print()
    print("## subscriptions to add category '{category}':".format(category=FEEDLY_CATEGORY))
    for x in todo['add_categories']:
        print(x)

    print()
    print("## subscriptions to remove category '{category}':".format(category=FEEDLY_CATEGORY))
    for x in todo['remove_categories']:
        print(x)


def _sync_to_feedly(feedly_client, qiidly_category_id, todo):
    for f in todo['subscribe_ids']:
        feedly_client.subscribe_feed(f, qiidly_category_id)
    if len(todo['unsubscribe_ids']) > 0:
        feedly_client.unsubscribe_feeds(todo['unsubscribe_ids'])
    to_update = todo['add_categories'] + todo['remove_categories']
    if len(to_update) > 0:
        feedly_client.update_feeds(to_update)


if __name__ == '__main__':
    args = _arg_parser().parse_args()

    qiita_token = args.qiita_token
    feedly_token = args.feedly_token

    # Qiita
    qiita_user_id = qiita.get_user_id(qiita_token)
    qiita_tag_feed_urls = qiita.get_following_tag_feed_urls(
        qiita_token,
        qiita_user_id)
    qiita_feed_ids = [feedly.to_feed_id(x) for x in qiita_tag_feed_urls]

    # Feedly
    feedly_client = feedly.FeedlyClient(feedly_token)
    feedly_user_profile = feedly_client.get_user_profile()

    feedly_user_id = feedly_user_profile['id']
    qiidly_category_id = feedly.to_category_id(feedly_user_id, FEEDLY_CATEGORY)

    subscriptions = feedly_client.get_user_subscriptions()

    # todo check
    todo = _create_todo(qiita_feed_ids, subscriptions)
    if _up_to_date(todo):
        print('Already up-to-date.')
        exit(0)
    _print_todo(todo)

    # sync to Feedly
    print('')
    if not _query_yes_no('Sync Feedly with your Qiita?', default=None):
        print('Did nothing.')
        exit(0)

    _sync_to_feedly(feedly_client, qiidly_category_id, todo)
    print('Done!')
