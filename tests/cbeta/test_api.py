#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.testcase import APITestCase
from controller.cbeta.meta import get_juan
from controller.cbeta.esearch import search


class TestApi(APITestCase):

    def test_api_mulu(self):
        """ 测试获取目录信息 """
        # 测试经号不带字母
        r = self.fetch('/api/cbeta/mulu', body={'data': dict(zang='T', jing='1579')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIsInstance(data.get('data'), list)
        # 测试经号带字母
        r = self.fetch('/api/cbeta/mulu', body={'data': dict(zang='T', jing='0181a')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIsInstance(data.get('data'), list)

    def test_api_get_juan(self):
        """ 测试获取目录信息 """
        juan = get_juan('T30n1579_p0299a01')
        self.assertEqual(juan, 5)

    def test_mod_search(self):
        """ 全文检索 """
        # 测试单个关键字及排序
        q = '彌勒'
        r1, total = search(q)
        self.assertIsNotNone(r1)
        r2, total = search(q, sort='page_code')
        self.assertIsNotNone(r2)
        self.assertGreater(float(r1[0]['score']), float(r2[0]['score']))

        # 测试检索page_code
        q = 'T30n1579_p0279'
        r3, total = search(q, field='page_code')
        self.assertIsNotNone(r3)

        # 测试指定经目范围
        sutra_codes = ['T0675', 'B0045']
        r4, total = search(q, filter_sutra_codes=sutra_codes)
        self.assertIsNotNone(r4)

    def test_api_search(self):
        """ 测试全文检索 """
        # 测试简单关键字
        r = self.fetch('/api/cbeta/search', body={'data': dict(q='菩薩', page='2')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIn('hits', data.get('data'))

    def test_api_img_url(self):
        """ 测试获取图片url """
        r = self.fetch('/api/cbeta/img_url', body={'data': dict(page_code='T52n2103_p0222')})
        self.assert_code(200, r)
        data = self.parse_response(r)
        self.assertIn('img_url', data.get('data'))

