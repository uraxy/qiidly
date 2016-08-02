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

    def test__to_tag_feed_url(self):
        tag = {
            "followers_count": 60,
            "icon_url": "https://s3-ap-northeast-1.amazonaws.com/qiita-tag-image/247db9e46df769906ad1093d71f994ad3f06617f/medium.jpg?1388309710",
            "id": "OpenCL",
            "items_count": 45
          }
        expected = 'http://qiita.com/tags/OpenCL/feed.atom'
        actual = qiidly.qiita._to_tag_feed_url(tag)
        self.assertEqual(expected, actual)
