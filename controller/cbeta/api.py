#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@time: 2019/07/30
"""

from controller import errors
import controller.validate as v
from controller.base import BaseHandler, DbError
from controller.cbeta.meta import get_mulu_info


class getMuluApi(BaseHandler):
    URL = '/api/mulu'

    def post(self):
        """ 获取目录信息"""
        try:
            data = self.get_request_data()
            rules = [
                (v.not_empty, 'zang', 'jing'),
                (v.is_zang, 'zang'),
                (v.is_jing, 'jing'),
            ]
            err = v.validate(data, rules)
            if err:
                return self.send_error_response(err)

            mulu_info = get_mulu_info(data['zang'], data['jing'])
            if mulu_info is False:
                return self.send_error_response(errors.mulu_not_found)

            self.send_data_response(mulu_info)

        except DbError as e:
            return self.send_db_error(e)
