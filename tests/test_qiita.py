# -*- coding: utf-8 -*-
import unittest
import qiidly.qiita


class TestQiita(unittest.TestCase):
    """Test for qiidly.qiita."""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tag_feed_url_from_tag_id(self):
        tag_id = 'OpenCL'
        expected = 'http://qiita.com/tags/OpenCL/feed.atom'
        actual = qiidly.qiita.tag_feed_url_from_tag_id(tag_id)
        self.assertEqual(expected, actual)

    def test_tag_id_from_tag_feed_url(self):
        tag_feed_url = 'http://qiita.com/tags/python/feed.atom'
        expected = 'python'
        actual = qiidly.qiita.tag_id_from_tag_feed_url(tag_feed_url)
        self.assertEqual(expected, actual)

    def test_user_feed_url_from_user_id(self):
        user_id = 'uraxy'
        expected = 'http://qiita.com/uraxy/feed.atom'
        actual = qiidly.qiita.user_feed_url_from_user_id(user_id)
        self.assertEqual(expected, actual)

    def test_user_id_from_user_feed_url(self):
        user_feed_url = 'http://qiita.com/uraxy/feed.atom'
        expected = 'uraxy'
        actual = qiidly.qiita.user_id_from_user_feed_url(user_feed_url)
        self.assertEqual(expected, actual)
