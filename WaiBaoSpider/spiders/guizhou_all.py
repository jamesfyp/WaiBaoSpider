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


class GuiZhouSSpider(scrapy.Spider):
    name = "guizhoubua"
    all_dict = {
        u"贵州六盘水": [4, "2018-05-21", 29853],
        u"六盘水六枝特区": [129, "2018-08-13", 22772],
    }
    base_url = "http://bjjs.gzegn.gov.cn/gzszwfww/cxsx/showcxlb.do?pageno={pn}&applyStartDate=2017-01-01&applyEndDate={std}&webId={id}"
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for info in self.all_dict:
            id = self.all_dict[info][0]
            std = self.all_dict[info][1]
            page_all = self.all_dict[info][2]
            dumper = CSVDumper(u"%s_buchonglist_2.csv" % info)
            url = self.base_url.format(pn=1, std=std, id=id)
            yield Request(url, callback=self.parse_list, headers=self.headers,
                          meta={"dump": dumper, "pn": 1, "wid": id, "std": std, "page_all": page_all})

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        data = response.meta
        dumper = data["dump"]
        pn = data["pn"]
        page_all = data["page_all"]
        wid = data["wid"]
        std = data["std"]
        lines = html.xpath("//div[@class='sec']/table/div[@id='tab1_link']/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"链接"] = info.xpath("./td[9]/a/@href")[0].strip() if info.xpath("./td[9]/a/@href") else ""
            item[u"办理编号"] = "'{}'".format(
                info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else "")
            item[u"受理部门"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"受理事项"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"办理环节"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"申请日期"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"办结日期"] = info.xpath("./td[7]/text()")[0].strip() if info.xpath("./td[7]/text()") else ""
            item[u"申请人"] = info.xpath("./td[8]/text()")[0].strip() if info.xpath("./td[8]/text()") else ""
            item[u"办理结果"] = info.xpath("./td[9]/a/text()")[0].strip() if info.xpath("./td[9]/a/text()") else ""
            dumper.process_item(item)
        if pn < page_all:
            pn += 2
            url = self.base_url.format(pn=pn, std=std, id=wid)
            yield Request(url, callback=self.parse_list, headers=self.headers,
                          meta={"dump": dumper, "pn": pn, "wid": wid, "std": std, "page_all": page_all})

