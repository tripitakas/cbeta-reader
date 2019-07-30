#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.testcase import APITestCase
from controller.cbeta.meta import get_juan


class TestApi(APITestCase):

    def test_api_mulu(self):
        """ 测试获取目录信息 """
        # 测试经号不带字母
        r = self.fetch('/api/mulu', body={'data': dict(zang='T', jing='1579')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIsInstance(data.get('data'), list)
        # 测试经号带字母
        r = self.fetch('/api/mulu', body={'data': dict(zang='T', jing='0181a')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIsInstance(data.get('data'), list)

    def test_api_get_juan(self):
        """ 测试获取目录信息 """
        juan = get_juan('T30n1579_p0299a01')
        self.assertEqual(juan, 5)
