# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
import re

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class ShaoGuanSpider(scrapy.Spider):
    name = "shaoguan"
    base_url = "https://wlwz.sg.gov.cn/website/wlwz/wlwzSiteAction!manyWzTitle.action?pattern=hot&areaCode=440200&style=all&currentpage={}&pagesize=20"
    base_detail_url = "https://wlwz.sg.gov.cn/website/wlwz/wlwzSiteAction!findTitleDetail.action?forward=wzxxDetail&themeid={}&areaCode={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
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
        for i in range(1, 1720):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='logintable']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"业务编号"] = info.xpath("./td[1]/span/text()")[0].strip() if info.xpath("./td/span/text()") else ""
            item[u"主题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"问政人"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"发起时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"状态"] = info.xpath("./td[5]/span/text()")[0].strip() if info.xpath("./td[5]/span/text()") else ""
            item[u"点击数"] = "'{}'".format(
                info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else "")
            links = info.xpath("./td[2]/a/@onclick")[0].strip() if info.xpath("./td[2]/a/@onclick") else ""
            links = re.search("'(\d+)','(\d+)'", links)
            if links:
                item[u"链接"] = self.base_detail_url.format(links.group(1), links.group(2))
                self.dump_list.process_item(item)
                yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers)
            else:
                item[u"链接"] = u""
                self.dump_list.process_item(item)

    def parse_detail(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        item = {}
        item[u"网友提问"] = deal_ntr(html.xpath("//td[@class='Friends_top']/span/text()")[0] if html.xpath(
            "//td[@class='Friends_top']/span/text()") else "")
        item[u"发言时间"] = deal_ntr(html.xpath("//td[@class='Friends_top1']/text()")[0] if html.xpath(
            "//td[@class='Friends_top1']/text()") else "")
        item[u"审核时间"] = deal_ntr(
            html.xpath("//div[@class='Friends_div']/div[@class='Friends_title1']/text()")[0].strip() if html.xpath(
                "//div[@class='Friends_div']/div[@class='Friends_title1']/text()") else "")
        item[u"审核时间"] = item[u"审核时间"].replace(u"审核时间：", u"")
        content = html.xpath("//div[@class='Friends_div']/div[1]//text()") if html.xpath(
            "//div[@class='Friends_div']/div[1]//text()") else []
        item[u"发言内容"] = deal_ntr("".join(content))
        item[u"受理单位"] = deal_ntr(html.xpath("//div[@class='Reply_title']/text()")[0].strip() if html.xpath(
            "//div[@class='Reply_title']/text()") else "")
        slr_slsj = html.xpath("(//td[@class='Reply_title1'])[2]/text()")[0].strip() if html.xpath(
            "(//td[@class='Reply_title1'])[2]/text()") else ""
        slr_slsj = slr_slsj.replace(u"受理人:", u"").replace(u"受理时间:", u"")
        slsj = re.search(u"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", slr_slsj)
        if slsj:
            item[u"受理时间"] = slsj.group()
        else:
            item[u"受理时间"] = u""
        item[u"受理人"] = deal_ntr(slr_slsj.replace(item[u"受理时间"], u""))
        hfr_hfsj = html.xpath("(//td[@class='Reply_title1'])[4]/text()")[0].strip() if html.xpath(
            "(//td[@class='Reply_title1'])[4]/text()") else ""
        hfr_hfsj = hfr_hfsj.replace(u"回复人:", u"").replace(u"回复时间:", u"")
        hfsj = re.search(u"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", hfr_hfsj)
        if hfsj:
            item[u"回复时间"] = hfsj.group()
        else:
            item[u"回复时间"] = u""
        item[u"回复人"] = deal_ntr(hfr_hfsj.replace(item[u"回复时间"], u""))
        re_content = html.xpath("(//div[@class='Reply_title4'])//text()") if html.xpath(
            "(//div[@class='Reply_title4'])//text()") else []
        item[u"回复内容"] = deal_ntr("".join(re_content))
        myd = html.xpath("(//div[@class='Reply_title5'])[1]/span/text()") if html.xpath(
            "(//div[@class='Reply_title5'])[1]/span/text()") else []
        item[u"满意度"] = deal_ntr("".join(myd))
        pingjia_time = html.xpath("//div[@class='Reply_title6']/text()")[0].strip() if html.xpath(
            "//div[@class='Reply_title6']/text()") else ""
        pingjia_time = re.search(u"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", pingjia_time)
        if pingjia_time:
            item[u"评价时间"] = pingjia_time.group()
        else:
            item[u"评价时间"] = u""
        self.dump_detail.process_item(item)
