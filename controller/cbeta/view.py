#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: CBETA阅读
@time: 2019/3/13
"""
import re
import os
from glob2 import glob
import lxml.etree as etree
import controller.errors as errors
from controller.base import BaseHandler
from controller.cbeta.meta import get_juan, get_juan_info, XML_DIR


class CbetaHandler(BaseHandler):
    URL = '/@code'

    re_logic = re.compile(r'^([A-Z]{1,2})([A-Z]?\d+[A-Za-z]?)(_(\d+))?$')
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
                return self.send_error_response(errors.sutra_code_error, render=True)

            # 获取卷信息
            juan_list = get_juan_info(zang, jing)
            if juan_list is False:
                return self.send_error_response(errors.juan_not_found, render=True)

            # 检查当前卷
            juan = 1 if juan < 1 else juan_list[-1] if juan_list and juan > juan_list[-1] else juan

            # 获取经文数据
            fuzzy_name = '%s*n%s_%03d.xml' % (zang, jing, int(juan))
            xml_file = glob(os.path.join(XML_DIR, 'ori', zang, '**', fuzzy_name))
            if not xml_file:
                return self.send_error_response(errors.xml_not_found, render=True)
            article = self.get_article(xml_file[0])

            index = juan_list.index(juan)
            prev = juan_list[1 if index < 1 else index - 1],
            next = juan_list[index + 1 if index < len(juan_list) - 1 else len(juan_list) - 1]
            self.render(
                'cbreader.html', article=article, code=code, zang=zang, jing=jing, juan=juan,
                juan_list=juan_list, prev=prev, next=next
            )

        except Exception as e:
            return self.send_db_error(e, render=True)

    @staticmethod
    def get_article(xml_file):
        """ 从xml_file中获取供前端展示的内容 """

        def replace(match):
            txt = match.group(0).replace('\n', '')
            return re.sub('[「」『』（），、：；。？！]', lambda m: '<bd>%s</bd>' % m.group(0), txt)

        xsl = open(os.path.join(os.path.dirname(__file__), 'taisho.xsl'), 'rb')
        xslt = etree.XML(xsl.read())
        transform = etree.XSLT(xslt)
        article = transform(etree.parse(xml_file))
        article = str(article)
        article = article[article.find('<body>') + 6: article.rfind('</body>')]
        re_text = r'<div class="text">([\s\S]*)</div>'
        article = re.sub(re_text, replace, article, flags=re.M)
        return article
