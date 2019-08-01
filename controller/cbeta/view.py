#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: CBETA阅读
@time: 2019/3/13
"""

from controller.cbeta.base import CbetaBaseHandler


class CbetaHandler(CbetaBaseHandler):
    URL = ['/@code',  '/']

    def get(self, code='T0001_001'):
        """ CBETA阅读和搜索 """
        try:
            args = self.get_sutra_content(code)
            self.render('cbreader.html', **args)

        except Exception as e:
            return self.send_db_error(e, render=True)
