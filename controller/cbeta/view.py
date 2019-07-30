#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: CBETA阅读
@time: 2019/3/13
"""
import re
import os
import json
from glob2 import glob
import lxml.etree as etree
import controller.errors as errors
from controller.base import BaseHandler
from controller.cbeta.meta import get_juan, XML_DIR, JUAN_DIR


class CbetaHandler(BaseHandler):
    URL = '/@code'

    re_logic = re.compile(r'^([A-Z]{1,2})(\d+)(_(\d+))?$')
    re_physical = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)([abc]\d+)?$')

    def get(self, code=''):
        """ CBETA阅读和搜索
        :param code编号：可以是经卷编号（逻辑编号），如T1579（大正藏第1579部经，即《瑜伽師地論》），或T1579_001（《瑜伽師地論》第一卷）；
            也可以是页编码或行编号（物理编号），如T30n1579_p0279、T30n1579_p0279a08（大正藏第30册第1579部经279页第a栏第8行） """
        try:
            if self.re_logic.match(code):
                m = self.re_logic.search(code)
                zang, jing, juan = m.group(1), m.group(2), m.group(4) and int(m.group(4)) or 1
            elif self.re_physical.match(code):
                m = self.re_physical.search(code)
                zang, jing, juan = m.group(1), m.group(3), get_juan(code)
            else:
                return self.send_error_response(errors.sutra_code_error)

            # 获取总卷数
            fuzzy_name = '%s*n%s.json' % (zang, jing)
            juan_file = glob(os.path.join(JUAN_DIR, zang, '**', fuzzy_name))
            if not juan_file:
                return self.send_error_response(errors.juan_not_found)
            with open(juan_file[0], 'r') as fp:
                juan_list = json.load(fp)
            juan_count = int(len(juan_list) / 2)

            # 检查卷数
            juan = 1 if juan < 1 else juan_count if juan > juan_count else juan

            # 获取经文数据
            fuzzy_name = '%s*n%s_%03d.xml' % (zang, jing, int(juan))
            xml_file = glob(os.path.join(XML_DIR, 'ori', zang, '**', fuzzy_name))
            if not xml_file:
                return self.send_error_response(errors.xml_not_found)
            article = self.get_article(xml_file[0])

            self.render(
                'cbreader.html', article=article, code=code, zang=zang, jing=jing, juan=juan, juan_count=juan_count,
            )

        except Exception as e:
            return self.send_db_error(e, render=True)

    @staticmethod
    def get_article(xml_file):
        """ 从xml_file中获取供前端展示的内容 """

        def replace(match):
            txt = match.group(0).replace('\n', '')
            return re.sub('[「」『』（），、：；。？！]', lambda m: '<bd>%s</bd>' % m.group(0), txt)

        xsl = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'taisho.xsl'), 'rb')
        xslt = etree.XML(xsl.read())
        transform = etree.XSLT(xslt)
        article = transform(etree.parse(xml_file))
        article = str(article)
        article = article[article.find('<body>') + 6: article.rfind('</body>')]
        re_text = r'<div class="text">([\s\S]*)</div>'
        article = re.sub(re_text, replace, article, flags=re.M)
        return article
