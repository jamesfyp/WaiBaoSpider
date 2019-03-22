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
    name = "guizhoubu"
    all_dict = {
        u"黔南州独山": [185, "2018-09-10"],
        u"黔南州福泉": [179, "2018-06-01"],
        u"黔南州荔波": [187, "2018-03-18"],
        u"黔南州平塘": [188, "2018-09-28"],
        u"黔南州三都": [186, "2018-11-30"],
        u"黔南州瓮安": [180, "2017-12-21"],
        u"黔南州长顺": [184, "2018-11-23"],
        u"黔西南册亨": [196, "2017-08-17"],
        u"黔西南晴隆": [195, "2017-11-30"],
        u"黔西南兴仁": [192, "2018-06-21"],
        u"黔西南兴义": [191, "2018-04-02"],
        u"黔西南贞丰": [194, "2017-11-22"],
        u"铜仁江口": [155, "2017-12-26"],
        u"铜仁石阡": [156, "2018-05-28"],
        u"铜仁松桃": [153, "2018-02-01"],
        u"铜仁印江": [157, "2018-12-26"],
        u"铜仁玉屏": [154, "2018-01-09"],
        u"遵义播州": [28, "2018-01-29"],
        u"遵义赤水": [38, "2018-07-24"],
        u"遵义汇川": [27, "2017-12-08"],
        u"遵义仁怀": [39, "2018-10-22"],
        u"遵义绥阳": [30, "2018-02-24"],
        u"遵义桐梓": [29, "2018-10-09"],
        u"遵义务川": [33, "2017-12-18"],
        u"遵义习水": [37, "2018-07-10"],
        u"遵义新蒲新": [127, "2017-12-19"],
        u"遵义余庆": [202, "2017-08-30"],
        u"遵义正安": [31, "2018-02-27"],
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
            pn += 1
            url = self.base_url.format(pn=pn, std=std, id=wid)
            yield Request(url, callback=self.parse_list, headers=self.headers,
                          meta={"dump": dumper, "pn": pn, "wid": wid, "std": std, "page_all": page_all})

