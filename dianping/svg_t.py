# coding=utf-8
"""
大众点评-svg字体
"""
import re

from lxml import etree

import requests

y_limit = []
single = ''


def get_text(svg_url):
    global y_limit
    print svg_url
    res = requests.get(svg_url)
    # print 'AAA', res.content
    word_box = []
    lines = re.findall('<text .*?>(.*?)</text>', res.text)
    y_limit = re.findall('<text x=".*" y="(\\d+)">', res.text)
    # print y_limit
    for line in lines:
        word_box.append(line.strip())
    # print word_box
    return word_box


def make_word(word_box, x, y):
    global y_limit
    x = abs(x)
    y = abs(y)
    # 计算字体处于那一行
    for k, v in enumerate(y_limit):
        # print 'HHH', k, v, y
        if int(v) > int(y):
            line = word_box[k]
            break
    else:
        line = []
    # 计算字体处于第几个字体,并得出结果
    x = x / 14
    return line[x]


def get_css(css_url):
    global single
    res = requests.get(css_url)
    # print res.content
    # 查找符号
    single = re.search('span\[class\^="(.*?)"', res.content).group(1)
    print single
    lists = re.findall('\.' + single + '(.*?)}', res.content)
    svg_url = re.findall('span\[class\^="'+single+'"].*?url\(//([0-9a-z_./]*\.svg?)\);', res.content)
    #print svg_url
    svg_url = 'https://' + svg_url[0]
    # print u'NAME LIST', lists
    print svg_url
    css_box = {}
    for lis in lists:
        name = single + re.search('(.*){', lis).group(1).decode('utf-8')
        cyb = re.findall('-(\\d+)\.0px', lis)
        css_box[name] = cyb
    print css_box
    return css_box, svg_url


def get_final(word_box, css_box):
    final_box = {}
    for k, v in css_box.iteritems():
        word = make_word(word_box, int(v[0]), int(v[1]))
        final_box[k] = word

    return final_box


def get_big_box(css_url):
    # 加载css
    css_box, svg_url = get_css(css_url)
    # 加载原始字体
    word_box = get_text(svg_url)
    print 'word box', word_box
    # css对应原始字体
    final_box = get_final(word_box, css_box)
    final_box["single"] = single
    print final_box
    return final_box


if __name__ == '__main__':
    # css = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/3828ad97bb7f256c413145bf1b89b775.css'
    css = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/97fe9c5b05f072c9bcd9c248fb69766d.css'
    get_big_box(css)
