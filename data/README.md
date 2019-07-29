# cbeta_build.py

从 BM_u8 提取每页的纯文本内容和页面元数据，并从 cbeta-juan 提取每页所在的卷信息，导出页面数据到 es。

如果以 `python3 data/cbeta_build.py --index=` 运行，则不导入到es，只做数据检查，将页面数据输出到 build_log。

页面数据字段：
```
page_code: 页名，由册别、经号、别本、页号组成，例如 A091n1057_p0319
canon_code: 藏经代码，例如 A、T
book_no: 册号，例如 091
book_code: 册别，藏经代码+册号，例如 A091、GA001
sutra_no: 经号，例如 1057、A042
sutra_code: 典籍编号，藏经代码+经号，例如 A1057
page_no: 页号，例如 0319、b005
cols: [[栏号, 起始栏列号, 起始文本行序号, 终止栏列号, 终止文本行序号]]，例如：
      [["a", "a01", 0, "a26", 25], ["b", "b01", 26, "b26", 51]]
juan: 本页的卷项数组[{"n": "001", "fun": "open", "head": "T03n0152_p0001a03", "title": "六度集經卷第一"},]
origin: 原始文本，部分组字式已替换为生僻字
normal: 规范文本，是对原始文本的异体字转换为规范字的结果
lines: 文本行数
char_count: 规范文本(含标点)的字数
updated_time: 入库时间
```

# 经meta
针对每部经而言，meta信息包括目录信息和卷信息两部分。这两部分信息从每部经对应的xml文件中提取生成。

## mulu
经的目录信息存放在目录文件夹下，按“藏/册/经/经名.json”的格式即进行定位。每部经都有对应的目录文件，如果该部经没有目录信息，则对应的json文件大小为0。

## juan
每部经都有其对应的卷信息，通过卷信息可以知道每部经有多少卷，每一卷从哪一行开始，到哪一行结束。


# 卷xml
网站阅读是以卷为单位进行的，卷xml文件下存放对应的数据，包括ori/zh_tw/zh三种类型。

## ori
将经xml按卷拆分，即可得到卷xml文件。

## zh_tw
对ori中的一些异体字或生僻字进行处理，替换为对应的正字，以便提供的更好的阅读服务。

## zh
将zh_tw中的繁体字进行处理，得到其简化字版本，以便提供简体字阅读服务。

# 相关文件
- [经xml文件](https://github.com/cbeta-org/xml-p5)
- [mulu](https://pan.baidu.com/s/1m43SofIdh6hoZ6-mIWnutw) (提取码: xd2f)
- [juan](https://pan.baidu.com/s/1cRwZaN2MlUnx7ATmsmG_5g) (提取码: gzft)
- [ori](https://pan.baidu.com/s/11wu8xFOw3rUF8mpQINdJog) (提取码: mpk9)
