# -*- coding: utf-8 -*-

import unittest
import qiidly.feedly


class TestFeedly(unittest.TestCase):
    """Test for qiidly.feedly

    Getting Started with Sandbox
    https://developer.feedly.com/v3/sandbox/

    OAuth clientId: sandbox
    OAuth clientSecret: CNKEATM7ICEGVOZ3P5A1 (expires on October 1st 2016)
    API_URL = 'https://sandbox.feedly.com'
    """

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

        # self.feedly_client = qiidly.feedly.FeedlyClient(self.TOKEN, self.API_URL)
        # print(self.TOKEN)
        # print(self.API_URL)

    def tearDown(self):
        pass
        # print()
        # print('>> tearDown method is called.')

    def test_feed_id_from_feed_url(self):
        feed_url = 'https://example.com/feed'
        expected = 'feed/https://example.com/feed'
        actual = qiidly.feedly.feed_id_from_feed_url(feed_url)
        self.assertEqual(expected, actual)

    def test_feed_url_from_feed_id(self):
        feed_id = 'feed/https://example.com/feed'
        expected = 'https://example.com/feed'
        actual = qiidly.feedly.feed_url_from_feed_id(feed_id)
        self.assertEqual(expected, actual)

    def test_category_id_from_user_id_and_category(self):
        USER_ID = 'UUU'
        CATEGORY = 'CCC'
        expected = 'user/UUU/category/CCC'
        actual = qiidly.feedly.category_id_from_user_id_and_category(USER_ID, CATEGORY)
        self.assertEqual(expected, actual)

    def test_category_from_category_id(self):
        cagegory_id = 'user/UUU/category/CCC'
        expected = 'CCC'
        actual = qiidly.feedly.category_from_category_id(cagegory_id)
        self.assertEqual(expected, actual)
