# -*- coding: utf-8 -*-
"""dummy docstring."""
import my_qiita
import my_feedly
import copy
import argparse


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
def query_yes_no(question, default=None):
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


def arg_parser():
    parser = argparse.ArgumentParser(description='qiidly: Qiita to Feedly.')
    parser.add_argument('-q', '--qiita-token',
                        required=True,
                        help='Qiita access token (https://qiita.com/settings/applications)')
    parser.add_argument('-f', '--feedly-token',
                        required=True,
                        help='Feedly developer access token (https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token)')
    return parser


if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    qiita_access_token = args.qiita_token
    feedly_access_token = args.feedly_token

    qiita_user_id = my_qiita.get_user_id(qiita_access_token)
    qiita_tags_feed_urls = my_qiita.get_following_tag_feed_urls(
        qiita_access_token,
        qiita_user_id)
    qiita_feed_ids = [my_feedly.to_feed_id(x) for x in qiita_tags_feed_urls]

    feedly_user_profile = my_feedly.get_user_profile(feedly_access_token)
    feedly_user_id = feedly_user_profile['id']
    subscriptions = my_feedly.get_user_subscriptions(feedly_access_token)

    qiidly_category_id = my_feedly.to_category_id(feedly_user_id, FEEDLY_CATEGORY)

    # for x in subscriptions:
    #     print(x)

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
    to_subscribe_ids = []
    to_add_category = []
    to_remove_category = []
    to_unsubscribe_ids = []
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
                    to_add_category.append(s)
                else:  # FEEDLY_CATEGORYがあれば、何もしなくて良い
                    pass
                break
        else:  # 1-2. Feedlyで購読なし -> 購読追加対象へ
            to_subscribe_ids.append(q)

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
            to_unsubscribe_ids.append(f_sub['id'])
            continue
        # 1個以上の場合は更新対象へ
        new_categs = [x for x in f_sub['categories'] if x['id'] != qiidly_category_id]
        s = {'title': f_sub['title'],
             'id': f_sub['id'],
             'categories': new_categs}
        to_remove_category.append(s)

    print('Feedlyに対して…')
    print('================')
    print('## 新規購読追加するもの：')
    print(to_subscribe_ids)
    print('## 購読を削除するもの：')
    print(to_unsubscribe_ids)
    print("## 登録済みの購読にカテゴリ'{category}を追加するもの".format(category=qiidly_category_id))
    for x in to_add_category:
        print(x)
    print("## 登録済みの購読からカテゴリ'{category}を削除するもの".format(category=qiidly_category_id))
    for x in to_remove_category:
        print(x)

    # ===== 最後は更新しますか(y/n)させたほうが良い。APIエラー対策。
    print('')
    if query_yes_no('Feedlyに反映していいですか？', default=None):
        for f in to_subscribe_ids:
            my_feedly.subscribe_feed(feedly_access_token, f, qiidly_category_id)
        if len(to_unsubscribe_ids) > 0:
            my_feedly.unsubscribe_feeds(feedly_access_token, to_unsubscribe_ids)
        to_update = to_add_category + to_remove_category
        if len(to_update) > 0:
            my_feedly.update_feeds(feedly_access_token, to_update)
        print('反映完了！')
    else:
        print('じゃ、反映やめとくね。')
