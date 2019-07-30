#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from glob2 import glob
import os.path as path
from lxml import etree
from datetime import datetime
from functools import cmp_to_key

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


def cmp(juan1, juan2):
    # n有两种情况，如1/1a
    if juan1['n'] == juan2['n']:
        return ['open', 'close'].index(juan1['fun']) - ['open', 'close'].index(juan2['fun'])
    elif re.sub('[a-z]', '', juan1['n']) == re.sub('[a-z]', '', juan2['n']):
        return re.sub('[0-9]', '', juan1['n']) > re.sub('[0-9]', '', juan2['n'])
    else:
        return re.sub('[a-z]', '', juan1['n']) > re.sub('[a-z]', '', juan2['n'])


def get_juan_from_xml(fn):
    """ 从xml文件中获取卷信息 """
    juan = []
    root = etree.parse(fn)
    namespaces = {'cb': 'http://www.cbeta.org/ns/1.0'}
    for item in root.xpath('//cb:juan', namespaces=namespaces):
        if item.xpath('@n'):
            # 获取行首
            lb_items = item.xpath('./preceding::*[@ed]')
            lb = lb_items[-1].xpath('@n') if lb_items else []
            head = '%s_p%s' % (path.basename(fn).split('.')[0], ','.join(lb))
            juan.append({'n': ','.join(item.xpath('@n')), 'fun': ','.join(item.xpath('@fun')), 'head': head})
    return juan.sort(key=cmp_to_key(cmp))


def order_juan(source=JUAN_DIR):
    """ 卷信息排序 """

    for fn in glob(path.join(source, '**', '*.json')):
        print('[%s]%s: processing... ' % ((datetime.now().strftime('%Y-%m-%d %H:%M:%S')), path.basename(fn)))
        if os.path.getsize(fn) == 0:
            continue
        with open(fn, 'r+') as fp:
            juan_list = json.load(fp)
            juan_list = [r for r in juan_list if r.get('n')]
            juan_list.sort(key=cmp_to_key(cmp))
            fp.seek(0)
            fp.truncate()
            json.dump(juan_list, fp)


if __name__ == '__main__':
    pass
