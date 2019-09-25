#!/usr/bin/python
# -*- coding: UTF-8 -*-
from html.parser import HTMLParser
from urllib import request
import ssl
# 取消ssl验证
ssl._create_default_https_context = ssl._create_unverified_context

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []


    def handle_starttag(self, tag, attrs):
        # print('star: <%s> 属性 %s' % (tag ,attrs))
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
        if tag == 'li' and _attr(attrs, 'data-title'):
            movie = {}
            movie['actors'] = _attr(attrs, 'data-actors')
            movie['actors'] = _attr(attrs, 'data-actors')
            movie['director'] = _attr(attrs, 'data-director')
            movie['duration'] = _attr(attrs, 'data-dutation')
            movie['title'] = _attr(attrs, 'data-title')
            movie['rate'] = _attr(attrs, 'data-rate')
            # print(_attr(attrs, 'data-actors'))
            self.movies.append(movie)


    def handle_endtag(self, tag):
        pass
        # print('end: </%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('startendtag :<%s/> 结尾属性 %s' % (tag,attrs))


    def handle_data(self, data):
        pass
        # print('所有data %s' % data)


    def handle_comment(self, data):
        pass
        # print('<!--', data, '-->')

    def handle_entityref(self, name):
        pass
        # print('&%s;' % name)

    def handle_charref(self, name):
        pass
        # print('&#%s;' % name)

def movieparser(url):
    myparser = MyHTMLParser()
    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')
        myparser.feed(data)
        myparser.close()

    return myparser.movies

if __name__ == '__main__':
    url = 'https://movie.douban.com/'
    movies = movieparser(url)
    for each in movies:
        print('%(title)s|%(rate)s|%(actors)s|%(director)s|%(duration)s' % each)