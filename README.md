# cbeta-reader

基于CBETA经论数据的藏经搜索和研阅平台，基于 Python3+Tornado、MongoDB、Elasticsearch+ik分词插件 开发。

[![CI](https://travis-ci.org/tripitakas/cbeta-reader.svg?branch=dev)](https://travis-ci.org/tripitakas/cbeta-reader)
[![Coverage](https://codecov.io/gh/tripitakas/cbeta-reader/branch/dev/graph/badge.svg)](https://codecov.io/gh/tripitakas/cbeta-reader)

## 安装

本平台需要 Python 3.6+，MongoDB 和 ES 可用远程数据库。

## 测试

本项目可采用测试驱动开发(TDD)模式实现后端接口和前端控制器类：

```
pip install -r tests/requirements.txt
python3 tests/add_pages.py --db_name=cbreader_test --reset=1
python3 run_tests.py 或选中测试用例文件调试
```

在 `tests` 下编写测试用例，然后在 `controller.views` 或 `controller.api` 中实现后端接口。

如果需要单独多次调试某个用例，可将 `run_tests.py` 中的 `test_args += ['-k test_` 行注释去掉，
改为相应的测试用例名，在用例或API响应类中设置断点调试。

## 参考资料

- [项目术语表](doc/glossary.md)

- [Bootstrap 3 中文文档](https://v3.bootcss.com)
- [Tornado 官方文档中文版](https://tornado-zh.readthedocs.io/zh/latest/)
- [Tornado 前端模板语法](https://tornado-zh.readthedocs.io/zh/latest/guide/templates.html)
- [Introduction to Tornado 中文版](http://demo.pythoner.com/itt2zh/)
- [MongoDB 数据库开发](http://demo.pythoner.com/itt2zh/ch4.html)
- [MongoDB 官方文档](http://api.mongodb.com/python/current/index.html)
- [MongoDB 查询操作符](https://docs.mongodb.com/manual/reference/operator/query/)
