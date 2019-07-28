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
