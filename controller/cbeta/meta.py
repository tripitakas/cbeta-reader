#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os.path as path
from glob2 import glob
from controller.app import BASE_DIR

XML_DIR = path.join(BASE_DIR, 'data', 'xml')
MULU_DIR = path.join(BASE_DIR, 'data', 'meta', 'mulu')
JUAN_DIR = path.join(BASE_DIR, 'data', 'meta', 'juan')


def get_juan(code):
    """
    根据code获取它属于第几卷
    :param code: 可以是行编码，也可以是页编码。比对时会根据code的长度进行比较，裁剪掉多余的部分
    :return: 大于0的卷号或False。有些卷信息中带有a/b/c等栏符，返回时过滤掉。
    """

    def cmp(page_code1, page_code2):
        # 裁剪到长度一致
        length = min(len(page_code1), len(page_code2))
        page_code1 = page_code1[0:length]
        page_code2 = page_code2[0:length]
        # 判断格式以及藏经类型是否一致
        h1 = regex.search(page_code1)
        h2 = regex.search(page_code2)
        if not h1 or not h2 or h1.group(1) != h2.group(1):
            return False
        # 将栏位转换为数字
        tran = dict(a='1', b='2', c='3')
        if h1.group(5):
            page_code1 = h1.group(1) + h1.group(2) + h1.group(3) + h1.group(4) + tran.get(h1.group(6)) + h1.group(7)
        if h2.group(5):
            page_code2 = h2.group(1) + h2.group(2) + h2.group(3) + h2.group(4) + tran.get(h2.group(6)) + h2.group(7)
        # 比较大小
        num1 = int(re.sub('[a-zA-Z_]', '', page_code1))
        num2 = int(re.sub('[a-zA-Z_]', '', page_code2))
        return num1 - num2

    regex = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+[A-Za-z]?)[A-Za-z_]?p([a-z]?\d+)(([abc])(\d+))?')
    head = regex.search(code)
    assert head and head.group(0)

    filename = '%sn%s.json' % (head.group(1) + head.group(2), head.group(3))
    json_file = path.join(JUAN_DIR, head.group(1), head.group(1) + head.group(2), filename)
    if path.exists(json_file) and path.getsize(json_file) > 2:
        with open(json_file, 'r') as fp:
            try:
                juan_list = json.load(fp)
            except ValueError as e:
                print('Fail to load json file(%s): %s' % (json_file, str(e)))
                return

        # 如果code小于第一卷
        if cmp(juan_list[0]['head'], code) >= 0:
            return int(re.sub('[a-z]', '', juan_list[0]['n']))

        # 如果code大于最末卷
        if cmp(juan_list[-1]['head'], code) <= 0:
            return int(re.sub('[a-z]', '', juan_list[-1]['n']))

        for i, juan in enumerate(juan_list[:-1]):
            next_j = juan_list[i + 1]
            if cmp(juan['head'], code) <= 0 <= cmp(next_j['head'], code):
                return int(re.sub('[a-z]', '', next_j['n']))

        return False


def get_juan_info(zang, jing, only_juan=True):
    """ 获取卷信息
    :param zang 藏代码，如T、GA等
    :param jing 经号，如1、01等
    :param only_juan 是否仅仅返回卷值"""
    fuzzy_name = '%s*n%s.json' % (zang, jing)
    juan_file = glob(path.join(JUAN_DIR, zang, '**', fuzzy_name))
    if not juan_file:
        return False
    if path.getsize(juan_file[0]) == 0:
        return []
    with open(juan_file[0], 'r') as fp:
        juan_info = json.load(fp)
        if only_juan:
            # 过滤掉卷值中的a/b/c等栏位信息
            juan_info = list(set(int(re.sub('[a-z]', '', i.get("n"))) for i in juan_info))
            juan_info.sort()
        return juan_info


def get_mulu_info(zang, jing):
    """ 获取目录信息
    :param zang 藏代码，如T、GA等
    :param jing 经号，如1、01等"""

    def add_node(node):
        _node = {k: v for k, v in node.items() if k in ['route', 'text', 'children']}
        _node['li_attr'] = {'title': node['head']}

        parent = tree
        for i in node.get('route').split('-')[:-1]:
            parent = parent['children'][int(i) - 1]

        if parent.get('children'):
            parent['children'].append(_node)
        else:
            parent['children'] = [_node]

    def format(mulu_list):
        """ 将从json文件中获取的目录信息格式化为层次结构
        依次扫描节点，根据当前节点的level和前一个节点的level的关系，设置route路由信息，然后根据路由信息构建树结构
        route路由信息：如'1-1-2'，表示第一棵树/第一个子节点/第二个子节点 """
        for i, mulu in enumerate(mulu_list):
            if int(mulu['level']) == 1:
                mulu['route'] = '%s' % (len(tree['children']) + 1)
                add_node(mulu)
                continue
            pre_mulu = mulu_list[i - 1]
            if int(mulu['level']) == int(pre_mulu['level']):
                r1, r2 = pre_mulu['route'].rsplit('-', 1)
                mulu['route'] = '%s-%s' % (r1, int(r2) + 1)
                add_node(mulu)
            elif int(mulu['level']) > int(pre_mulu['level']):
                mulu['route'] = pre_mulu['route'] + '-1'
                add_node(mulu)
            elif int(mulu['level']) < int(pre_mulu['level']):
                # 根据当前mulu的level，从pre_mulu的路由中截取对应长度的路由信息
                pre_route = '-'.join(pre_mulu['route'].split('-')[: int(mulu['level'])])
                r1, r2 = pre_route.rsplit('-', 1)
                mulu['route'] = '%s-%s' % (r1, int(r2) + 1)
                add_node(mulu)

    fuzzy_name = '%s*n%s.json' % (zang, jing)
    mulu_file = glob(path.join(MULU_DIR, zang, '**', fuzzy_name))
    if not mulu_file:
        return False
    if path.getsize(mulu_file[0]) == 0:
        return []
    with open(mulu_file[0], 'r') as fp:
        tree = {'level': 0, 'children': []}
        format(json.load(fp))
        return tree['children']

