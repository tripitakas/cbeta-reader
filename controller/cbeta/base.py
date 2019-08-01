#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: 全文检索基类
@time: 2019/8/1
"""

import re
import os
from glob2 import glob
import lxml.etree as etree
import controller.errors as errors
from controller.base import BaseHandler
from controller.cbeta.meta import get_juan, get_juan_info, XML_DIR
import logging


class CbetaBaseHandler(BaseHandler):

    logic_code = re.compile(r'^([A-Z]{1,2})([A-Z]?\d+[A-Za-z]?)(_(\d+))?$')
    physical_code = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)([abc]\d+)?$')

    def get_sutra_content(self, code='T0001_001'):
        """
        获取经文内容
        :param code编号：可以是经卷编号（逻辑编号），如T1579（大正藏第1579部经，即《瑜伽師地論》），或T1579_001（《瑜伽師地論》第一卷）；
                也可以是页编码或行编号（物理编号），如T30n1579_p0279、T30n1579_p0279a08（大正藏第30册第1579部经279页第a栏第8行）
        """
        render = '/api' not in self.request.path
        if self.logic_code.match(code):
            m = self.logic_code.search(code)
            zang, jing, juan = m.group(1), m.group(2), m.group(4) and int(m.group(4)) or 1
        elif self.physical_code.match(code):
            m = self.physical_code.search(code)
            zang, jing, juan = m.group(1), m.group(3), get_juan(code)
        else:
            return self.send_error_response(errors.sutra_code_error, render=render)

        if not juan:
            return self.send_error_response(errors.juan_not_found, render=render)

        # 获取卷信息
        juan_list = get_juan_info(zang, jing)
        if juan_list is False:
            return self.send_error_response(errors.juan_not_found, render=render)

        # 检查当前卷
        juan = 1 if juan < 1 else juan_list[-1] if juan_list and juan > juan_list[-1] else juan

        # 获取经文数据
        fuzzy_name = '%s*n%s_%03d.xml' % (zang, jing, int(juan))
        xml_file = glob(os.path.join(XML_DIR, 'ori', zang, '**', fuzzy_name))
        if not xml_file:
            logging.warning('ori/%s not exist' % fuzzy_name)
            return self.send_error_response(errors.xml_file_not_found, render=render)
        content = self.tran_xml(xml_file[0])
        logging.info(','.join([code, xml_file[0]]))

        if juan in juan_list:
            index = juan_list.index(juan)
            prev = len(juan_list) > 1 and juan_list[0 if index < 0 else index - 1]
            next = juan_list[index + 1 if index < len(juan_list) - 1 else len(juan_list) - 1]
        else:
            prev = juan - 1 or 1
            next = juan + 1
        return dict(
            content=content, code=code, zang=zang, jing=jing, juan=juan,
            juan_list=juan_list, prev=prev, next=next
        )


    @staticmethod
    def tran_xml(xml_file):
        """ 将经文的xml文件转换html """

        def format_bd(match):
            """ 设置标点 """
            txt = match.group(0).replace('\n', '')
            return re.sub('[「」『』（），、：；。？！]', lambda m: '<bd>%s</bd>' % m.group(0), txt)

        xsl = os.path.join(os.path.dirname(__file__), 'taisho.xsl')
        xslt = etree.XML(open(xsl, 'rb').read())
        transform = etree.XSLT(xslt)
        article = transform(etree.parse(xml_file))
        article = str(article)
        article = article[article.find('<body>') + 6: article.rfind('</body>')]
        re_text = r'<div class="text">([\s\S]*)</div>'
        article = re.sub(re_text, format_bd, article, flags=re.M)
        return article
