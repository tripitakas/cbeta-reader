#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from glob2 import glob
import os.path as path
from lxml import etree
from datetime import datetime

XML_P5_DIR = './xml/xml-p5'
MULU_DIR = './meta/mulu'
JUAN_DIR = './meta/juan'


def extract_mulu_from_xml_p5(source=XML_P5_DIR, overwrite=False):
    """ 从CBETA xml-p5中提取目录信息 """
    for fn in glob(path.join(source, '**', '*.xml')):
        print('[%s]%s: processing... ' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
        # 检查目录信息是否已存储
        head = re.search(r'^([A-Z]{1,2})(\d+)n(.*)', path.basename(fn))
        assert head and head.group()
        to_dir = path.join(MULU_DIR, head.group(1), head.group(1) + head.group(2))
        if not path.exists(to_dir):
            os.makedirs(to_dir)
        to_file = path.join(to_dir, path.splitext(path.basename(fn))[0] + '.json')
        if not overwrite and path.exists(to_file):
            print('[%s]%s: mulu file existed! ' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
            continue

        # 获取目录信息，然后写文件
        mulu = get_mulu_from_xml(fn)
        print(
            '[%s]%s: mulu file has been written.' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
        with open(to_file, 'w') as fp:
            if mulu:
                json.dump(mulu, fp, ensure_ascii=False)
            else:
                fp.write('')


def get_mulu_from_xml(fn):
    """ 从xml文件中获取目录信息 """

    def fast_iter(context, func):
        for event, elem in context:
            func(elem)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

    def get_mulu(item):
        if item.xpath('@type') != ['卷']:
            # 获取行首
            lb_items = item.xpath('./preceding::*[@ed]')
            lb = lb_items[-1].xpath('@n') if lb_items else []
            head = '%s_p%s' % (path.basename(fn).split('.')[0], ','.join(lb))
            info = {
                'level': ','.join(item.xpath('@level')),
                'n': ','.join(item.xpath('@n')),
                'type': ','.join(item.xpath('@type')),
                'text': ','.join(item.xpath('text()')),
                'head': head
            }
            mulu.append(info)

    mulu = []
    context = etree.iterparse(fn, events=('end',), tag='{http://www.cbeta.org/ns/1.0}mulu')
    fast_iter(context, get_mulu)
    return mulu


def extract_juan_from_xml_p5(source=XML_P5_DIR, overwrite=False):
    """ 从CBETA xml-p5中提取卷信息 """
    for fn in glob(path.join(source, '**', '*.xml')):
        print('[%s]%s: processing... ' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
        # 检查卷信息是否已存储
        head = re.search(r'^([A-Z]{1,2})(\d+)n(.*)', path.basename(fn))
        assert head and head.group()
        to_dir = path.join(JUAN_DIR, head.group(1), head.group(1) + head.group(2))
        if not path.exists(to_dir):
            os.makedirs(to_dir)
        to_file = path.join(to_dir, path.splitext(path.basename(fn))[0] + '.json')
        if not overwrite and path.exists(to_file):
            print('[%s]%s: juan file existed! ' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
            continue

        # 获取卷信息，然后写文件
        juan = get_juan_from_xml(fn)
        print(
            '[%s]%s: juan file has been written.' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
        with open(to_file, 'w') as fp:
            if juan:
                json.dump(juan, fp, ensure_ascii=False)
            else:
                fp.write('')


def get_juan_from_xml(fn):
    """ 从xml文件中获取卷信息 """
    juan = []
    root = etree.parse(fn)
    namespaces = {'cb': 'http://www.cbeta.org/ns/1.0'}
    for item in root.xpath('//cb:juan', namespaces=namespaces):
        # 获取行首
        lb_items = item.xpath('./preceding::*[@ed]')
        lb = lb_items[-1].xpath('@n') if lb_items else []
        head = '%s_p%s' % (path.basename(fn).split('.')[0], ','.join(lb))
        juan.append({
            'n': ','.join(item.xpath('@n')),
            'fun': ','.join(item.xpath('@fun')),
            'head': head
        })
    return juan


def get_juan(code, source_type="json"):
    """ 根据code获取它属于第几卷。
    :param code code可以是行编码，也可以是页编码。比对时会根据code的长度进行比较，裁剪掉多余的部分
    :param source_type xml表示xml文本，json表示是从xml文件中提取的json信息"""

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

    regex = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+[A-Za-z]?)_p([a-z]?\d+)(([abc])(\d+))?')
    head = regex.search(code)
    assert head and head.group(0)
    if source_type == 'xml':
        filename = '%sn%s.xml' % (head.group(1) + head.group(2), head.group(3))
        xml_file = path.join(XML_P5_DIR, head.group(1), head.group(1) + head.group(2), filename)
        juan_list = get_juan_from_xml(xml_file)
    else:
        filename = '%sn%s.json' % (head.group(1) + head.group(2), head.group(3))
        json_file = path.join(JUAN_DIR, head.group(1), head.group(1) + head.group(2), filename)
        with open(json_file, 'r') as fp:
            juan_list = json.load(fp)

    # 如果code小于第一卷
    if cmp(juan_list[0]['head'], code) >= 0:
        return 1
    # 如果code大于最末卷
    if cmp(juan_list[-1]['head'], code) <= 0:
        return juan_list[-1]['n']

    for i, juan in enumerate(juan_list[:-1]):
        next = juan_list[i + 1]
        if cmp(juan['head'], code) <= 0 <= cmp(next['head'], code):
            return int(next['n'])

    return False


if __name__ == '__main__':
    juan = get_juan('B06n0009_p0451')
    print(juan)
