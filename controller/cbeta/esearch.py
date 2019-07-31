#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from controller.cbeta.diff import Diff
from elasticsearch import Elasticsearch
from controller.cbeta.variant import normalize
from controller.app import Application as App


def get_hosts():
    config = App.load_config()
    return [config.get('esearch', {})]


def can_search():
    hosts = get_hosts()
    return hosts[0].get('host')


def pre_filter(q):
    q = normalize(q)
    q = re.sub(r'[\x00-\xff]', '', q)
    q = re.sub(Diff.junk_cmp_str, '', q)
    return q


def format_hits(hits, shrink=True):
    """ 格式化检索结果
    :param shrink 是否缩起来 """

    def merge_kw(txt):
        # 将<kw>一</kw>，<kw>二</kw>格式替换为<kw>一，二</kw>
        regex = r'[，、：；。？！“”‘’「」『』（）%&*◎—……]+'
        txt = re.sub('</kw>(%s)<kw>' % regex, lambda r: r.group(1), txt)
        # 合并相邻的关键字
        txt = re.sub('</kw><kw>', '', txt)
        return txt

    def shrink(txt):
        """ 将检索结果缩起来，以便前端显示 """
        s, e = txt.find('<kw>'), txt.rfind('</kw>')
        return '<div class="shrink">%s</div>%s<div class="shrink">%s</div>' % (txt[:s], txt[s:e + 5], txt[e + 5:])

    for i, hit in enumerate(hits):
        if 'highlight' in hit:
            highlights = {re.sub('</?kw>', '', v): merge_kw(v) for v in hit['highlight']['normal']}
            normal = [highlights.get(r, r) for r in hit['_source']['normal']]
        else:
            normal = hit['_source']['normal']
        normal = ''.join(normal)
        hits[i] = {
            'score': hit['_score'],
            'page_code': hit['_source'].get('page_code'),
            'sutra_code': hit['_source'].get('sutra_code'),
            'normal': shrink(normal) if shrink else normal,
        }

    return hits


def search(q, field='normal', page=1, sort='score', filter_sutra_codes=None, index='cb4ocr-ik'):
    """ 从ES中寻找与q最匹配的document
    :param field 查询哪个字段，normal表示规范文本字段，page_code表示页码
    :param page 第几页
    :param sort 排序方式，score表示相似度，page_code表示页码
    :param filter_sutra_codes 查询经号的范围
    :param index 查询哪个索引
    """
    if not q or not can_search():
        return []

    q = pre_filter(q) if field == 'normal' else q
    sort = [{'page_code': 'asc'}, '_score'] if sort == 'page_code' else ['_score', {'page_code': 'asc'}]
    highlight = {'pre_tags': ['<kw>'], 'post_tags': ['</kw>'], 'fields': {'normal': {}}}
    dsl = {
        'size': 10,
        'from': 10 * (int(page) - 1),
        'sort': sort,
        'highlight': highlight,
        'query': {
            'bool': {
                'must': {
                    'match': {field: q}
                }
            }
        },
    }
    if filter_sutra_codes:
        dsl['query']['bool']['filter'] = [{'terms': {'sutra_code': filter_sutra_codes}}]

    es = Elasticsearch(hosts=get_hosts())
    r = es.search(index=index, body=dsl)
    hits, total = r['hits']['hits'], r['hits']['total']['value']
    hits = format_hits(hits)
    return hits, total
