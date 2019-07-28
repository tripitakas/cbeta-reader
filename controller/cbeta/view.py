#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: CBETA阅读
@time: 2019/3/13
"""
import os
import lxml.etree as etree
from controller.base import BaseHandler


class CbetaHandler(BaseHandler):
    URL = '/'

    def get(self):
        """ CBETA """
        xsl = open('%s/taisho.xsl' % os.path.dirname(os.path.realpath(__file__)), 'rb')
        xslt = etree.XML(xsl.read())
        transform = etree.XSLT(xslt)
        xml = etree.parse(os.path.join(self.application.BASE_DIR, 'static/xml/T/T10/T10n0279_001._xml'))
        content = transform(xml)
        article = str(content)
        article = article[article.find('<body>') + 6: article.rfind('</body>')]
        self.render('tripitaka_cbeta.html', article=article)