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


class ChenZhouSpider(scrapy.Spider):
    name = "chenzhou"
    base_url = "http://www.app.czs.gov.cn/webapp/czs/email2015/index.jsp?login=true&cflag=1&type=0&stype=0&ext_5=&ext_6=&emailList.offset={}&emailList.desc=false"
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
        while i < 9895:
            # while i < 2:
            url = self.base_url.format(i)
            print(i)
            i += 5
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("(//div[@class='lxfk-bd'])[1]/dl")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"标题"] = info.xpath("./dt/a/text()")[0].strip() if info.xpath("./dt/a/text()") else ""
            item[u"链接"] = info.xpath("./dt/a/@href")[0].strip().replace(u"..",
                                                                        u"http://www.app.czs.gov.cn/webapp/czs") if info.xpath(
                "./dt/a/@href") else ""
            item[u"来信人"] = info.xpath("./dt/span/text()")[0].strip().replace(u"来信人：", u"") if info.xpath(
                "./dt/span/text()") else ""
            item[u"来信时间"] = info.xpath("./dt/span/i/text()")[0].strip() if info.xpath("./dt/span/i/text()") else ""
            item[u"回复部门"] = info.xpath("./dd/a/text()")[0].strip() if info.xpath("./dd/a/text()") else ""
            hfsj = info.xpath("./dd/text()") if info.xpath("./dd/text()") else []
            hfsj = re.search(u"\d{4}-\d{2}-\d{2}", "".join(hfsj), re.DOTALL)
            if hfsj:
                item[u"回复时间"] = hfsj.group()
            else:
                item[u"回复时间"] = u""
            item[u"满意度"] = deal_ntr(info.xpath("./dd/span/text()")[0].strip().replace(u"满意度：", u"") if info.xpath(
                "./dd/span/text()") else "")
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "myd": item[u"满意度"], "hfbm": item[u"回复部门"], "xxr": item[u"来信人"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        the_body = html.xpath("//table[@class='ton_td2']/tr/td/table")[0]
        item = {}
        title = the_body.xpath("./tr[2]//text()") if the_body.xpath("./tr[2]//text()") else []
        item[u"标题"] = deal_ntr("".join(title))
        content = the_body.xpath("./tr[2]//text()") if the_body.xpath("./tr[2]//text()") else []
        item[u"正文"] = deal_ntr("".join(content))
        item[u"写信人"] = data["xxr"]
        item[u"写信时间"] = the_body.xpath("./tr[6]//tr[2]/td[2]/text()")[0].strip() if the_body.xpath(
            "./tr[6]//tr[2]/td[2]/text()") else ""
        re_content = the_body.xpath("./tr[13]//text()") if the_body.xpath("./tr[13]//text()") else []
        item[u"回复内容"] = deal_ntr("".join(re_content))
        item[u"回复部门"] = data["hfbm"]
        item[u"回信时间"] = the_body.xpath("./tr[15]//tr[2]/td[2]/text()")[0].strip() if the_body.xpath(
            "./tr[15]//tr[2]/td[2]/text()") else ""
        item[u"满意度"] = data["myd"]
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
