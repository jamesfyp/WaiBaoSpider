# coding=utf-8
"""
大众点评-svg字体
"""
import re

from lxml import etree

import requests


class DZDPSvg(object):

    def __init__(self):
        self.single = ""
        self.num_y = {}
        self.word_box = []
        self.final_box = {}

    def get_css_svg(self, css_url):
        res = requests.get(css_url) \
            # 查找符号
        self.single = re.search('span\[class\^="(.*?)"', res.content).group(1)
        print self.single
        lists = re.findall('\.' + self.single + '(.*?)}', res.content)
        svg_url = re.findall('span\[class\^="' + self.single + '"].*?url\(//([0-9a-z_./]*\.svg?)\);', res.content)
        svg_url = 'https://' + svg_url[0]
        # print u'NAME LIST', lists
        print svg_url
        css_box = {}
        for lis in lists:
            name = self.single + re.search('(.*){', lis).group(1).decode('utf-8')
            cyb = re.findall('-(\\d+)\.0px', lis)
            css_box[name] = cyb
        print css_box
        return css_box, svg_url

    def get_text(self, svg_url):
        print svg_url
        res = requests.get(svg_url).content
        html = etree.HTML(res)
        lines1 = html.xpath("//defs/path")
        print("------len %s" % len(lines1))
        for i in lines1:
            y = re.search("M0 (\d+) H600", i.xpath("./@d")[0]).group(1)
            y = int(y) - 23
            k_y = i.xpath("./@id")[0]
            self.num_y[y] = k_y
        lines2 = html.xpath("//textpath")
        print("------len %s" % len(lines2))
        for i in lines2:
            self.word_box.append(i.xpath("./text()")[0].strip())

    def get_final(self, css_box):
        for k, v in css_box.iteritems():
            x = int(v[0]) / 14
            y = int(self.num_y[int(v[1])]) - 1
            self.final_box[k] = self.word_box[y][x]
        self.final_box["single"] = self.single
        return self.final_box


def get_big_box2(css):
    dz_svg = DZDPSvg()
    css_box, svg_url = dz_svg.get_css_svg(css)
    dz_svg.get_text(svg_url)
    final_box = dz_svg.get_final(css_box)
    return final_box


if __name__ == '__main__':
    css = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/97fe9c5b05f072c9bcd9c248fb69766d.css'
    # css = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/4335bf0081572b25c762cfb1552ae041.css'
    big_box = get_big_box2(css)
    print(big_box)
