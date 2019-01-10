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


class HuaiAnSpider(scrapy.Spider):
    name = "huaian"
    base_url = "http://admin.huaian.gov.cn/web/center/zmhd/cms6/yjfk.jsp?page={}"
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
        for i in range(1, 4182):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='kuang_1']/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"主题"] = info.xpath("./td[1]/p/a/@title")[0].strip() if info.xpath("./td[1]/p/a/@title") else ""
            item[u"提交时间"] = info.xpath("./td[2]/p/text()")[0].strip() if info.xpath("./td[2]/p/text()") else ""
            item[u"办结时间"] = info.xpath("./td[3]/p/text()")[0].strip() if info.xpath("./td[3]/p/text()") else ""
            item[u"受理人(单位)"] = info.xpath("./td[4]/p/text()")[0].strip() if info.xpath("./td[4]/p/text()") else ""
            item[u"状态"] = info.xpath("./td[5]/p/text()")[0].strip() if info.xpath("./td[5]/p/text()") else ""
            item[u"链接"] = "http://admin.huaian.gov.cn{}".format(
                info.xpath("./td[1]/p/a/@href")[0].strip() if info.xpath("./td[1]/p/a/@href") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"标题"] = html.xpath("//td[@background]/table/tr[1]/td[2]/p/text()")[0].strip() if html.xpath(
            "//td[@background]/table/tr[1]/td[2]/p/text()") else ""
        item[u"内容"] = html.xpath("//td[@background]/table/tr[2]/td[2]/p/text()")[0].strip() if html.xpath(
            "//td[@background]/table/tr[2]/td[2]/p/text()") else ""
        item[u"处理结果"] = html.xpath("//td[@background]/table/tr[3]/td[2]/p/text()")[0].strip() if html.xpath(
            "//td[@background]/table/tr[3]/td[2]/p/text()") else ""
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
