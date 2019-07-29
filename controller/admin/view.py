#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: 首页
@time: 2018/6/23
"""

from controller.base import BaseHandler
from controller.helper import get_date_time
from controller.op_type import get_op_def, op_in_recent_trends


class AdminHandler(BaseHandler):
    URL = '/admin'

    def get(self):
        """ 后台管理页面 """
        try:
            user_id = self.current_user['_id']
            visit_count = self.db.log.count_documents({'create_time': {'$gte': get_date_time('%Y-%m-%d 00:00:00')},
                                                       'user_id': user_id, 'type': 'visit'})
            r = list(self.db.log.find({'user_id': user_id, 'type': {'$in': ['login_ok', 'register']}},
                                      {'create_time': 1}).sort('create_time', -1).limit(2))
            last_login = r and r[0]['create_time'][:16] or ''

            time = get_date_time('%Y-%m-%d 00:00:00', diff_seconds=-86400 * 5)
            rs = list(self.db.log.find({'create_time': {'$gte': time}})
                      .sort('create_time', -1).limit(100))
            recent_trends, user_trends = [], {}
            for t in rs:
                if not op_in_recent_trends(t['type']):
                    continue
                # 每个人的操作记录中，忽略一分钟内的连续记录
                time = t['create_time'][:15]  # 15:到分钟
                if user_trends.get(t['user_id']) == time:
                    continue
                user_trends[t['user_id']] = time

                context, params = '', {}
                d = get_op_def(t['type'], params)
                if d:
                    msg = d.get('msg', d['name'])
                    context = msg
                recent_trends.append(dict(time=t['create_time'][5:16], user=t.get('nickname'), context=context[:20]))

            self.render('admin.html', visit_count=1 + visit_count, last_login=last_login,
                        recent_trends=recent_trends[:7])
        except Exception as e:
            self.send_db_error(e, render=True)
