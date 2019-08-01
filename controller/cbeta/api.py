#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@time: 2019/07/30
"""
import re
from controller import errors
import controller.validate as v
from controller.cbeta.esearch import search
from controller.base import BaseHandler, DbError
from controller.cbeta.meta import get_mulu_info
from controller.cbeta.define import canon_maps


class GetMuluApi(BaseHandler):
    URL = '/api/cbeta/mulu'

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
                return self.send_error_response(errors.mulu_file_not_found)

            self.send_data_response(mulu_info)

        except DbError as e:
            return self.send_db_error(e)


class SearchApi(BaseHandler):
    URL = '/api/cbeta/search'

    def post(self):
        """ 全文检索 """
        try:
            data = self.get_request_data()
            rules = [
                (v.not_empty, 'q'),
                (v.is_digit, 'page'),
            ]
            err = v.validate(data, rules)
            if err:
                return self.send_error_response(err)

            m = re.match(r'^([A-Z]{1,2}\d+?n[A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)$', data['q'])
            field = 'page_code' if m else 'normal'
            page = int(data.get('page', 1))
            sort = data.get('sort', 'score')
            filter_sutra_codes = data.get('filter_sutra_codes')
            hits, total = search(data['q'], field=field, page=page, sort=sort, filter_sutra_codes=filter_sutra_codes)
            self.send_data_response({'hits': hits, 'total': total})

        except DbError as e:
            return self.send_db_error(e)
        except Exception as e:
            return self.send_error_response(e)


class PrevPageApi(BaseHandler):
    URL = '/api/cbeta/prev_page'

    def post(self):
        """ 上一页 """
        try:
            data = self.get_request_data()
            rules = [
                (v.not_empty, 'cur_page_code'),
                (v.is_page_code, 'cur_page_code'),
            ]
            err = v.validate(data, rules)
            if err:
                return self.send_error_response(err)

            cur_page_code = data['cur_page_code']
            head = re.search(r'^([A-Z]{1,2}\d+?n[A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)', cur_page_code)
            cur_page_no = head.group(2)
            prev_page_no = str(int(cur_page_no) - 1).zfill(len(cur_page_no))
            prev_page_code = '%s_p%s' % (head.group(1), prev_page_no)
            r, total = search(prev_page_code, field='page_code')
            if total == 0:
                return self.send_error_response(errors.no_result)

            self.send_data_response(r[0])

        except DbError as e:
            return self.send_db_error(e)
        except Exception as e:
            return self.send_error_response(e)


class NextPageApi(BaseHandler):
    URL = '/api/cbeta/next_page'

    def post(self):
        """ 下一页 """
        try:
            data = self.get_request_data()
            rules = [
                (v.not_empty, 'cur_page_code'),
                (v.is_page_code, 'cur_page_code'),
            ]
            err = v.validate(data, rules)
            if err:
                return self.send_error_response(err)

            cur_page_code = data['cur_page_code']
            head = re.search(r'^([A-Z]{1,2}\d+?n[A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)', cur_page_code)
            cur_page_no = head.group(2)
            prev_page_no = str(int(cur_page_no) + 1).zfill(len(cur_page_no))
            prev_page_code = '%s_p%s' % (head.group(1), prev_page_no)
            r, total = search(prev_page_code, field='page_code')
            if total == 0:
                return self.send_error_response(errors.no_result)

            self.send_data_response(r[0])

        except DbError as e:
            return self.send_db_error(e)
        except Exception as e:
            return self.send_error_response(e)


class getImgUrlApi(BaseHandler):
    URL = '/api/cbeta/img_url'

    canon_suffix_png = ['TS']

    def post(self):
        """ 下一页 """
        try:
            data = self.get_request_data()
            rules = [
                (v.not_empty, 'page_code'),
                (v.is_page_code, 'page_code'),
            ]
            err = v.validate(data, rules)
            if err:
                return self.send_error_response(err)

            img_url = ''
            head = re.search(r'^([A-Z]{1,2})(\d+)n[A-Z]?\d+[A-Za-z]?_p([a-z]?\d+)', data['page_code'])
            if canon_maps.get(head.group(1)) and canon_maps.get(head.group(1))[0]:
                zang = canon_maps.get(head.group(1))[0]
                suffix = 'png' if zang in self.canon_suffix_png else 'jpg'
                img_code = '%s_%s_%s' % (zang, head.group(2).strip('0'), head.group(3).strip('0'))
                img_url = self.get_img(img_code, suffix)

            self.send_data_response({'img_url': img_url})

        except DbError as e:
            return self.send_db_error(e)
