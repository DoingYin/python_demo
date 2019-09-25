#!/usr/bin/python
# -*- coding: UTF-8 -*-

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if (tag == 'div'):
            if (len(attrs) > 0):
                for (attr, value) in attrs:
                    if (attr == 'class' and value == 'ns_area list'):
                        print(attrs)
            else:
                pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        pass
        # print(data)

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass