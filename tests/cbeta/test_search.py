#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.testcase import APITestCase
from controller.cbeta.esearch import can_search


class TestSearch(APITestCase):

    def test_view_cbeta_search(self):
        if not can_search():
            return
        q = '夫宗極絕於稱謂賢聖以之沖默玄旨非言'
        r = self.fetch('/data/cbeta/search?q=%s&_no_auth=1' % q)
        self.assert_code(200, r)
        r = self.parse_response(r)
        self.assertIn('B33n0192_p0188', r)

