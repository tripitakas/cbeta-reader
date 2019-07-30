#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nohup python3 /home/sm/cbeta/code/data/build_meta.py >> /home/sm/cbeta/cbeta.log 2>&1 &
# python3 data/cbeta_build.py --bm_path=BM_u8_path
# 执行前，需要将 cbeta-juan、cbeta-mulu 放到本文件的目录下。
#
# 查看实际导入的数量: curl 'localhost:9200/_cat/indices?v'
# 查看最近导入的日志: python3 -c "print(''.join(open('/home/sm/cbeta/cbeta.log').readlines()[-5:]))"
# 停止导入任务: sudo kill -9 `ps -ef | grep cbeta_build.py | grep -v grep | awk -F" " {'print $2'}` 2

import re
import sys
import json
from os import path
from glob2 import glob
from datetime import datetime
from functools import partial

sys.path.append(path.dirname(path.dirname(__file__)))  # 为了使用下列controller模块

from controller.app import Application
from controller.cbeta.variant import normalize
from controller.cbeta.rare import format_rare
from controller.cbeta.meta import get_juan
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException

config = Application.load_config()['esearch']
BM_PATH = config.get('BM_u8') or '/home/sm/cbeta/BM_u8'
juan_path = path.join(path.dirname(__file__), 'cbeta-juan')
re_head_parts = re.compile(r'^([A-Z]{1,2})(\d+)n([A-Z]?\d+)([A-Za-z_]?)p([a-z]?\d+)([a-z]\d+)?')
output = dict(pages=[])


def junk_filter(txt):
    txt = re.sub('<[^>]*>', '', txt)
    txt = re.sub(r'\[.>(.)\]', lambda m: m.group(1), txt)
    txt = re.sub(r'\[[\x00-\xff＊]*\]', '', txt)
    return txt


def cur_time():
    return datetime.now().strftime('[%H:%M:%S]')


def add_page(index, rows, page_code, juan, line=0):
    if rows:
        origin = [format_rare(r) for r in rows]
        normal = [normalize(r) for r in origin]
        count = sum(len(r) for r in normal)
        if count > 15000 or len(origin) > 5000:  # 跳过大文件
            sys.stderr.write('%s\tfailed:\t%s\t%s lines\t %s chars\tout of limit\n' % (
                cur_time(), page_code, len(rows), count))
            return False

        canon_code = book_no = sutra_no = edition = page_no = None  # 藏经代码, 册号，经号，别本, 页码
        head = re_head_parts.search(page_code)  # ^([A-Z]{1,2})(\d+)n([A-Z]?\d+)([A-Za-z_]?)p([a-z]?\d+)
        if head:
            canon_code, book_no, sutra_no, edition, page_no = [head.group(i) for i in range(1, 6)]
            book_code, sutra_code = canon_code + book_no, canon_code + sutra_no
        if not juan and index is None:
            sys.stderr.write('juan not found: %s\n' % page_code)

        try:
            '''
            page_code: 页名，由册别、经号、别本、页号组成，例如 A091n1057_p0319
            canon_code: 藏经代码，例如 A、T
            book_no: 册号，例如 091
            book_code: 册别，藏经代码+册号，例如 A091、GA001
            sutra_no: 经号，例如 1057、A042
            sutra_code: 典籍编号，藏经代码+经号，例如 A1057
            page_no: 页号，例如 0319、b005
            juan: 本页的卷号
            origin: 原始文本，部分组字式已替换为生僻字
            normal: 规范文本，是对原始文本的异体字转换为规范字的结果
            lines: 文本行数
            char_count: 规范文本(含标点)的字数
            updated_time: 入库时间
            '''
            if index is not None:
                index(body=dict(
                    page_code=page_code, canon_code=canon_code, book_no=book_no, book_code=book_code, juan=juan,
                    sutra_no=sutra_no, sutra_code=sutra_code, edition=edition, page_no=page_no,
                    origin=origin, normal=normal, lines=len(rows), char_count=count, updated_time=datetime.now())
                )
            else:
                output['pages'].append(dict(page_code=page_code, juan=juan, origin=[origin[0], origin[-1]],
                                            lines=len(rows), char_count=count))
                if line < 0:
                    codes = [p['page_code'] for p in output['pages']]
                    with open('build.log', 'a') as f:
                        f.write('%s %d pages\n%s\n' % (
                            book_code, len(output['pages']), ', '.join(codes)))
                    with open(path.join(path.dirname(__file__), 'build_log', page_code + '.json'), 'w') as f:
                        json.dump(output['pages'], f, ensure_ascii=False)
                    output['pages'] = []
            if line > 0 and 0:
                sys.stdout.write('%d %s, ' % (line, page_code[len(book_code):]))
            elif line < 0 and 0:
                sys.stdout.write(page_code + '\n')
            return True
        except ElasticsearchException as e:
            sys.stderr.write('err %s: %s\n,' % (page_code, str(e)))
            return False


def scan_and_index_dir(index, source, book_code):
    """直接导入目录中的文本数据"""
    errors = []
    for i, fn in enumerate(sorted(glob(path.join(source, '**', r'new.txt')))):
        if book_code and '/%s/' % book_code not in fn:
            continue
        with open(fn, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        rows, page_code = [], None
        count = idx = total = 0
        sutra_id = juan = ''

        for row in lines:
            texts = re.split('#{1,3}', row.strip(), 1)
            if len(texts) != 2:
                continue
            head = re_head_parts.search(texts[0])
            col_line = head and head.group(6)
            if head:
                page_code_ = head.group(0)[:-len(col_line)]
                if page_code and page_code != page_code_:
                    count += 1
                    total += len(rows)
                    juan = get_juan(page_code) or juan
                    if not add_page(index, rows, page_code, juan, count):
                        errors.append(page_code)
                    rows = []
                    idx = 0
                    sutra_id_ = re.sub(r'[A-Za-z_]?p.+$', '', page_code_)
                    if sutra_id != sutra_id_:
                        sutra_id = sutra_id_
                page_code = page_code_
            else:
                print('head error:\t%s' % row)

            rows.append(junk_filter(texts[1]))
            idx += 1

        juan = get_juan(page_code) or juan
        if not add_page(index, rows, page_code, juan, -1):
            errors.append(page_code)
        elif rows:
            count += 1
            total += len(rows)
        sys.stdout.write('%s %s %d pages, %d lines\n' % (cur_time(), fn, count, total))

    if errors:
        with open(path.join(source, datetime.now().strftime('error-%Y%m%d-%H%M.json')), 'w') as f:
            json.dump(errors, f)
        print('%s error pages\n%s' % (len(errors), errors))


def build_db(index='cb4ocr-ik', bm_path=BM_PATH, mode='create', book_code='', split='ik'):
    """ 基于CBETA文本创建索引，以便ocr寻找比对文本使用
    :param index: 索引名称，为空时可做数据遍历检查，不导入到es库
    :param bm_path: BM_u8文本目录
    :param mode: 'create'表示新建，'update'表示更新
    :param book_code: 仅导入指定册别的页面
    :param split: 中文分词器的名称，如'ik'或'jieba'
    """
    es = index and Elasticsearch(hosts=[config])
    if not es:
        return scan_and_index_dir(None, bm_path, book_code)

    if mode == 'create':
        es.indices.delete(index=index, ignore=[400, 404])
        es.indices.create(index=index, ignore=400)
    else:
        es.indices.open(index=index, ignore=400)

    if split == 'ik':
        mapping = {'properties': {
            'normal': {'type': 'text', 'analyzer': 'ik_max_word', 'search_analyzer': 'ik_smart'},
            'origin': {'type': 'text', 'analyzer': 'ik_max_word', 'search_analyzer': 'ik_smart'},
        }}
        es.indices.put_mapping(index=index, body=mapping)
    elif split == 'jieba':
        mapping = {'properties': {
            'normal': {'type': 'text', 'analyzer': 'jieba_index', 'search_analyzer': 'jieba_index'},
            'origin': {'type': 'text', 'analyzer': 'jieba_index', 'search_analyzer': 'jieba_index'},
        }}
        es.indices.put_mapping(index=index, body=mapping)

    scan_and_index_dir(partial(es.index, index=index, ignore=[]), bm_path, book_code)


if __name__ == '__main__':
    import fire

    fire.Fire(build_db)
