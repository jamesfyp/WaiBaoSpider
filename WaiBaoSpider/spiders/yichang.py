# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: yichang.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import re
import os


class YiChangSpider(scrapy.Spider):
    name = "yichang"
    base_url = "http://hfrx.cn3x.com.cn/index.php?m=case&c=list&t=3&s=1&page={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        # 'DOWNLOAD_DELAY': 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for i in range(1, 189):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, headers=self.headers, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@id='a2']//table[@id='a2']/tr")[:-1]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件编号"] = "'{}'".format(
                info.xpath("./td[1]/div/text()")[0].strip() if info.xpath("./td[1]/div/text()") else "")
            item[u"来信标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"类型"] = info.xpath("./td[3]/div/text()")[0].strip() if info.xpath("./td[3]/div/text()") else ""
            item[u"提交时间"] = info.xpath("./td[4]/div/text()")[0].strip() if info.xpath("./td[4]/div/text()") else ""
            item[u"回复时间"] = info.xpath("./td[5]/div/text()")[0].strip() if info.xpath("./td[5]/div/text()") else ""
            item[u"链接"] = "http://hfrx.cn3x.com.cn/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/text()") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "xjbh": item[u"信件编号"], "lx": item[u"类型"], "title": item[u"来信标题"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"编号"] = data["xjbh"]
        zhuangtai = html.xpath("(//td[@class='WZ'])[1]/strong/text()")[0].strip() if html.xpath(
            "(//td[@class='WZ'])[1]/strong/text()") else ""
        zhuangtai = re.search(u"状态：(.*)", zhuangtai)
        if zhuangtai:
            item[u"状态"] = zhuangtai.group(1)
        else:
            item[u"状态"] = u""
        item[u"类别"] = data["lx"]
        item[u"标题"] = data["title"]
        tjsj_dqsj = html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[1]/td//td[3]/text()")[
            0].strip() if html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[1]/td//td[3]/text()") else ""
        tjsj = re.search(u"提交时间：(\d{4}-\d{2}-\d{2})", tjsj_dqsj)
        if tjsj:
            item[u"提交时间"] = tjsj.group(1)
        else:
            item[u"提交时间"] = u""
        dqsj = re.search(u"到期时间：(\d{4}-\d{2}-\d{2})", tjsj_dqsj)
        if dqsj:
            item[u"到期时间"] = dqsj.group(1)
        else:
            item[u"到期时间"] = u""
        content = html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[2]/td//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[2]/td//text()") else []
        item[u"来信内容"] = deal_ntr("".join(content).strip())
        tiwenzhe = html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[3]/td//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[1]/tr[2]/td/table/tr[3]/td//text()") else []
        item[u"提问者"] = deal_ntr("".join(tiwenzhe).replace(u"提问者：", u""))
        item[u"回复单位"] = html.xpath("(//td[@class='WZ'])[3]/strong/text()")[0].strip() if html.xpath(
            "(//td[@class='WZ'])[3]/strong/text()") else ""
        re_content = html.xpath(
            "(//td[@valign='top'])[1]/table[3]/tr[2]/td/table/tr[1]//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[3]/tr[2]/td/table/tr[1]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(re_content))
        hf_time = html.xpath(
            "(//td[@valign='top'])[1]/table[3]/tr[2]/td/table/tr[2]//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[3]/tr[2]/td/table/tr[2]//text()") else []
        item[u"回复时间"] = "".join(hf_time).strip().replace(u"回复时间：", u"")
        pingjia = html.xpath("(//td[@valign='top'])[1]/table[5]/tr[2]//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[5]/tr[2]//text()") else []
        item[u"评价"] = deal_ntr("".join(pingjia).strip())
        base_string = u"满意{}基本满意{}不满意{}"
        s1 = html.xpath("(//div[@class='WZ'])[1]/text()")[0].strip() if html.xpath(
            "(//div[@class='WZ'])[1]/text()") else u" "
        s2 = html.xpath("(//div[@class='WZ'])[2]/text()")[0].strip() if html.xpath(
            "(//div[@class='WZ'])[2]/text()") else u" "
        s3 = html.xpath("(//p[@class='WZ'])/text()")[0].strip() if html.xpath("(//p[@class='WZ'])/text()") else u" "
        item[u"其他评价"] = base_string.format(s1, s2, s3)
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
