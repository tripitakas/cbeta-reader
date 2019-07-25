#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.testcase import APITestCase
from controller import role
from controller import validate as v


class TestRole(APITestCase):
    def test_func(self):
        self.assertTrue(role.can_access('用户管理员', '/user/admin', 'GET'))
        self.assertFalse(role.can_access('', '/api/user/profile', 'POST'))

        self.assertEqual(role.get_route_roles('/user/role', 'GET'), ['用户管理员'])

        routes = role.get_role_routes('用户管理员, 数据管理员')
        self.assertIn('/api/user/my/(pwd|profile)', routes)

    def test_validate(self):
        data = {'name': '1234567890', 'phone': '', 'email': '', 'password': '', 'age': 8}
        rules = [
            (v.not_empty, 'name', 'password'),
            (v.not_both_empty, 'phone', 'email'),
            (v.is_name, 'name'),
            (v.is_phone, 'phone'),
            (v.is_email, 'email'),
            (v.is_password, 'password'),
            (v.between, 'age', 10, 100),
        ]

        errs = v.validate(data, rules)
        self.assertEqual(set(errs.keys()), {'age', 'email', 'name', 'password', 'phone'})
        for k, t in errs.items():
            self.assertIs(t.__class__, tuple)
            self.assertIs(t[0].__class__, int)
            self.assertIs(t[1].__class__, str)

    def test_all_roles(self):
        roles = role.get_all_roles('数据管理员,用户管理员')
        should = {'普通用户', '数据管理员', '用户管理员'}
        self.assertEqual(set(roles), should)
