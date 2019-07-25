#!/usr/bin/env python
# -*- coding: utf-8 -*-

op_types = {
    'visit': dict(name='页面访问'),
    'visit_err': dict(name='无效访问'),
    'login_no_user': dict(name='账号不存在'),
    'login_fail': dict(name='账号密码不对'),
    'login_ok': dict(name='登录成功', trends=True),
    'logout': dict(name='注销登录'),
    'register': dict(name='注册账号', trends=True),
    'change_user_profile': dict(name='修改用户信息'),
    'change_role': dict(name='修改用户角色'),
    'reset_password': dict(name='重置密码'),
    'delete_user': dict(name='删除用户'),
    'change_password': dict(name='修改个人密码'),
    'change_profile': dict(name='修改个人信息'),
}


def get_op_def(op_type, params=None):
    return op_types[op_type]


def get_op_name(op_type):
    return get_op_def(op_type)['name']


def op_in_recent_trends(op_type):
    return get_op_def(op_type).get('trends')
