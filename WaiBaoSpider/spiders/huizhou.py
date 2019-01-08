# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class HuiZhouSpider(scrapy.Spider):
    name = "huizhou"
    base_url = "http://www.huizhou.gov.cn/wlwzlist.shtml?method=letters4bsznList3&pager.offset={}"
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
        i = 0
        while i < 31511:
            # while i < 2:
            print(i)
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)
            i += 20

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("(//td[@valign='top'])[1]/table[2]/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"主题"] = info.xpath("./td[2]/a/@title")[0].strip() if info.xpath("./td[2]/a/@title") else ""
            item[u"来信人"] = deal_ntr(info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else "")
            item[u"办理时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"处理状态"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"回复单位"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"来信人评议"] = info.xpath("./td[7]/text()")[0].strip() if info.xpath("./td[7]/text()") else ""
            item[u"群众评议"] = deal_ntr(
                info.xpath("./td[8]/script/text()")[0].strip() if info.xpath("./td[8]/script/text()") else "")
            item[u"链接"] = "http://www.huizhou.gov.cn/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"list_item": item})

    def parse_detail(self, response):
        body = unicode_body(response)
        list_item = response.meta["list_item"]
        html = etree.HTML(body)
        item = {}
        item[u"来信人"] = list_item[u"来信人"]
        item[u"来信主题"] = list_item[u"主题"]
        item[u"受文单位"] = deal_ntr(
            html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[3]/td[2]/text()")[
                0].strip() if html.xpath(
                "//td[@background]/table/tr[2]/td/table[1]/tr[3]/td[2]/text()") else "")
        item[u"来信时间"] = html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[3]/td[4]/text()")[
            0].strip() if html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[3]/td[4]/text()") else ""
        item[u"来信类型"] = html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[4]/td[2]/text()")[
            0].strip() if html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[4]/td[2]/text()") else ""
        blzt = html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[4]/td[4]//text()") if html.xpath(
            "//td[@background]/table/tr[2]/td/table[1]/tr[4]/td[4]//text()") else []
        item[u"办理状态"] = deal_ntr("".join(blzt))
        lxnr = html.xpath("//td[@background]/table/tr[2]/td/table[1]/tr[5]/td[2]//text()") if html.xpath(
            "//td[@background]/table/tr[2]/td/table[1]/tr[5]/td[2]//text()") else []
        item[u"来信内容"] = deal_ntr("".join(lxnr))
        item[u"回文单位"] = html.xpath("//td[@background]/table/tr[2]/td/table[3]/tr[1]/td[2]/text()")[
            0].strip() if html.xpath("//td[@background]/table/tr[2]/td/table[3]/tr[1]/td[2]/text()") else ""
        item[u"办理时间"] = html.xpath("//td[@background]/table/tr[2]/td/table[3]/tr[2]/td[2]/text()")[
            0].strip() if html.xpath("//td[@background]/table/tr[2]/td/table[3]/tr[2]/td[2]/text()") else ""
        cljg = html.xpath(
            "//td[@background]/table/tr[2]/td/table[3]/tr[3]/td[2]//text()") if html.xpath(
            "//td[@background]/table/tr[2]/td/table[3]/tr[3]/td[2]//text()") else []
        item[u"处理结果"] = deal_ntr("".join(cljg))
        item[u"链接"] = list_item[u"链接"]
        list_item[u"回复单位"] = item[u"受文单位"]
        self.dump_list.process_item(list_item)
        self.dump_detail.process_item(item)
