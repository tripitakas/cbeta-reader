#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.testcase import APITestCase
from controller.data.rare import format_rare
from controller.data.variant import normalize


class TestSpecialText(APITestCase):

    def test_format_rare(self):
        rare = '测[尸@工]试[仁-二+戾]一[少/兔]下[乳-孚+卓]看[束*束]看'
        txt = '测𡰱试㑦一㝹下𠃵看𣗥看'
        self.assertEqual(format_rare(rare), txt)

    def test_variant_normalize(self):
        variants = '鼶𪕬𪕧𪕽𪕻测𪕊𪕑䶅𪕘试𪕓𪕗看黑𪐫黒𪐗看'
        normal = normalize(variants)
        txt = '鼶鼶鼶鼶鼶測𪕊𪕊䶅䶅試𪕓𪕓看黑黑黑黑看'
        self.assertEqual(normal, txt)
