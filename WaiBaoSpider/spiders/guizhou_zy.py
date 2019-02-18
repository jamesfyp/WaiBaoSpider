# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body
import os


class GuiZhouSSpider(scrapy.Spider):
    name = "guizhou_gy_ky"
    base_url = "http://www.gzegn.gov.cn/gzszwfww/cxsx/showcxlb.do?pageno={}&webId=21"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    # dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for i in range(1, 3448):
            print(i)
            # for i in range(1, 2):
            # self.data_form["pageID"] = str(i)
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='sec']/table/div[@id='tab1_link']/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"链接"] = info.xpath("./td[9]/a/@href")[0].strip() if info.xpath("./td[9]/a/@href") else ""
            item[u"办理编号"] = info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else ""
            item[u"受理部门"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"受理事项"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"办理环节"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"申请日期"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"办结日期"] = info.xpath("./td[7]/text()")[0].strip() if info.xpath("./td[7]/text()") else ""
            item[u"申请人"] = info.xpath("./td[8]/text()")[0].strip() if info.xpath("./td[8]/text()") else ""
            item[u"办理结果"] = info.xpath("./td[9]/a/text()")[0].strip() if info.xpath("./td[9]/a/text()") else ""
            self.dump_list.process_item(item)
