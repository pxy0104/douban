# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
"""
1.Tag 标签及其内容
2.NavigableString 标签内的内容，字符串
3.BeautifulSoup 文档内容
4.Comment 返回内容不包含注释符号
"""

# file = open("./Top 250.html","rb")
# html = file.read()
# bs = BeautifulSoup(html,"html.parser")
# print(type(bs.title.string))
# print((bs.a).string)
#print(bs.head)

# print(bs)
# print(bs.head.contents)
col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价人数", "概况", "相关信息")
print(len(col))