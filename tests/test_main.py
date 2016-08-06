# -*- coding: utf-8 -*-
import unittest
import qiidly.main


class TestMain(unittest.TestCase):
    """Test for qiidly.main"""

    @classmethod
    def setUpClass(cls):
        pass
        # print()
        # print('> setUpClass method is called.')

    @classmethod
    def tearDownClass(cls):
        pass
        # print()
        # print('> tearDownClass method is called.')

    def setUp(self):
        pass
        # print()
        # print('>> setUp method is called.')

    def tearDown(self):
        pass
        # print()
        # print('>> tearDown method is called.')

    def test_tag_feed_url_from_tag_id(self):
        feed_id = 'feed/http://qiita.com/tags/OpenCL/feed.atom'
        expected = 'OpenCL'
        actual = qiidly.main.tag_id_from_feed_id(feed_id)
        self.assertEqual(expected, actual)

    # def _create_todo(qiita_feed_ids, subscriptions):
    #
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

    # def test__create_todo(self):
    #     qiidly_category_id = 'DUMMY'
    #     qiita_feed_ids = ['feed/http://qiita.com/tags/onsenui/feed.atom']
    #     subscriptions = []
    #     expected = []
    #     actual = qiidly.main._create_todo(qiidly_category_id, qiita_feed_ids, subscriptions)
    #     print(actual)
    #     self.assertEqual(expected, actual)
