#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@desc: 角色和权限
@time: 2019/3/13
角色权限对应表，定义系统中的所有角色以及对应的route权限。
将属于同一业务的route分配给同一个角色，用户通过拥有角色来拥有对应的route权限。
角色可以嵌套定义，如下表中的切分专家和文字专家。
"""

import re

url_placeholder = {
    'code': r'[A-Z]{1,2}\d+\w+',
    'sutra_code': r'[A-Z]{1,2}\d+',
    'page_name': r'[a-zA-Z]{2}_[0-9_]+',
    'page_prefix': r'[a-zA-Z]{2}[0-9_]*',
}

""" 角色列表。
针对每个角色定义：routes，角色可以访问的权限集合；roles，角色所继承的父角色；is_assignable，角色是否可被分配
"""
role_maps = {
    '单元测试用户': {
        'routes': {
            '/api/user/list': ['GET'],
        }
    },
    '访客': {
        'remark': '任何人都可访问，无需登录',
        'routes': {
            '/': ['GET'],
            '/@code': ['GET'],
            '/help': ['GET'],
            '/api/cbeta/mulu': ['POST'],
            '/api/cbeta/search': ['POST'],
            '/api/cbeta/prev_page': ['POST'],
            '/api/cbeta/next_page': ['POST'],
            '/user/(login|register)': ['GET'],
            '/api/user/(login|logout|register)': ['POST'],
        }
    },
    '普通用户': {
        'remark': '登录用户均可访问，无需授权',
        'routes': {
            '/user/my/profile': ['GET'],
            '/api/user/my/(pwd|profile)': ['POST'],
            '/api/user/(avatar|email_code|phone_code)': ['POST'],
        }
    },
    '用户管理员': {
        'is_assignable': True,
        'roles': ['普通用户'],
        'routes': {
            '/api': ['GET'],
            '/api/code/(.+)': ['GET'],
            '/admin': ['GET'],
            '/user/(admin|role)': ['GET'],
            '/api/user/(delete|role|profile|reset_pwd)': ['POST'],
        }
    },
}

# 界面可分配的角色、切分审校和文字审校角色
assignable_roles = [role for role, v in role_maps.items() if v.get('is_assignable')]


def get_role_routes(role, routes=None):
    """
    获取指定角色对应的route集合
    :param role: 可以是一个或多个角色，多个角色为逗号分隔的字符串
    """
    assert type(role) == str, str(role)
    routes = dict() if routes is None else routes
    roles = [r.strip() for r in role.split(',')]
    for r in roles:
        for url, m in role_maps.get(r, {}).get('routes', {}).items():
            routes[url] = list(set(routes.get(url, []) + m))
        # 进一步查找嵌套角色
        for r0 in role_maps.get(r, {}).get('roles', []):
            get_role_routes(r0, routes)
    return routes


def can_access(role, path, method):
    """
    检查角色是否可以访问某个请求
    :param role: 可以是一个或多个角色，多个角色为逗号分隔的字符串
    :param path: 浏览器请求path
    :param method: http请求方法，如GET/POST
    """
    def match_exclude(p, exclude):
        for holder, regex in url_placeholder.items():
            if holder not in exclude:
                p = p.replace('@' + holder, '(%s)' % regex)
        route_accessible = get_role_routes(role)
        for _path, _method in route_accessible.items():
            for holder, regex in url_placeholder.items():
                if holder not in exclude:
                    _path = _path.replace('@' + holder, '(%s)' % regex)
            if (p == _path or re.match('^%s$' % _path, p) or re.match('^%s$' % p, _path)) and method in _method:
                return True
            parts = re.search(r'\(([a-z|]+)\)', _path)
            if parts:
                whole, parts = parts.group(0), parts.group(1).split('|')
                for ps in parts:
                    ps = _path.replace(whole, ps)
                    if (p == ps or re.match('^%s$' % ps, p) or re.match('^%s$' % p, ps)) and method in _method:
                        return True
    if match_exclude(path, []):
        return True
    if match_exclude(path, ['page_name']):
        return True
    return False


def get_route_roles(uri, method):
    roles = []
    for role in role_maps:
        if can_access(role, uri, method) and role not in roles:
            roles.append(role)
    return roles


def get_all_roles(user_roles):
    if isinstance(user_roles, str):
        user_roles = [u.strip() for u in user_roles.split(',')]
    roles = list(user_roles)
    for role in user_roles:
        sub_roles = role_maps.get(role, {}).get('roles')
        if sub_roles:
            roles.extend(sub_roles)
            for _role in sub_roles:
                roles.extend(get_all_roles(_role))
    return list(set(roles))
