#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
import re
from html.parser import HTMLParser

# handle_startendtag 处理开始标签和结束标签
# handle_starttag 处理开始标签，比如<xx>
# handle_endtag 处理结束标签，比如</xx>
# handle_charref 处理特殊字符串，就是以&#开头的，一般是内码表示的字符
# handle_entityref 处理一些特殊字符，以&开头的，比如
# handle_data 处理数据，就是<xx>data</xx>中间的那些数据
# handle_comment 处理注释
# handle_decl 处理<!开头的，比如<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
# handle_pi 处理形如<?instruction>的东西
class MyHTMLParser(HTMLParser):

    resultData = list()

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.infos = []
        self.index = 1

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
        if (tag == 'a' and len(attrs) > 0 and _attr(attrs, 'href')):
            info = {}
            info['index'] = self.index
            info['href'] = _attr(attrs, 'href')
            info["title"] = _attr(attrs, 'title')
            if (not _attr(attrs, 'title')):
                info['title'] = ''
            self.infos.append(info)
            self.index += 1

    def handle_data(self, data):
        if data:
            return data

def getHtmlData(url):
    # 请求
    request = urllib.request.Request(url)

    # 结果
    response = urllib.request.urlopen(request)
    data = response.read()
    data = data.decode('gbk')
    return data


# print(type(data))
# print(data)
testHtml = '''<html>
                <head></head>
                <body>
                <!-- test html parser -->
                <p>
                    Some 
                    <a href="#">html</a> 
                    HTML&nbsp;tutorial...<br>
                    END
                </p>
                </body>
            </html>'''

if __name__ == "__main__":
    url = 'http://news.163.com/domestic/'
    data = getHtmlData(url)
    parser = MyHTMLParser()
    parser.feed(data)
    print(parser.infos)
