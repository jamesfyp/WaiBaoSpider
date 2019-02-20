# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: changsha.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class ChangShaSpider(scrapy.Spider):
    name = "changsha"
    base_url = "http://wlwz.changsha.gov.cn/webapp/cs/email/index.jsp?cflag=1&emailList.offset={}&emailList.desc=false"
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
        i = 0
        while i < 57108:
            # while i < 2:
            print(i)
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)
            i += 12

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='table1']/tr")[1:-1]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = "'{}'".format(info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"主题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"链接"] = "http://wlwz.changsha.gov.cn/webapp/cs/email/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            item[u"信件类别"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"处理时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"处理部门"] = info.xpath("./td[5]/a/text()")[0].strip() if info.xpath("./td[5]/a/text()") else ""
            item[u"来信人"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "lxr": item[u"来信人"], "clbm": item[u"处理部门"], })

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"浏览量"] = html.xpath("//div[@class='current1']/p/span/text()")[0].strip().replace(u"浏览量：",
                                                                                               u"") if html.xpath(
            "//div[@class='current1']/p/span/text()") else ""
        item[u"标题"] = html.xpath("//div[@class='mailbox_title']/text()")[0].strip() if html.xpath(
            "//div[@class='mailbox_title']/text()") else ""
        content = html.xpath(
            "(//div[@class='letter_content1'])[1]/div[@class='specific_letter']//text()") if html.xpath(
            "(//div[@class='letter_content1'])[1]/div[@class='specific_letter']//text()") else []
        item[u"来信内容"] = deal_ntr("".join(content).strip())
        item[u"来信人"] = data["lxr"]
        item[u"来信时间"] = html.xpath("(//div[@class='specific_letter_bottom'])[1]/span[1]/text()")[
            0].strip() if html.xpath(
            "(//div[@class='specific_letter_bottom'])[1]/span[1]/text()") else ""
        re_content = html.xpath(
            "(//div[@class='letter_content1'])[2]/div[@class='specific_letter']//text()") if html.xpath(
            "(//div[@class='letter_content1'])[2]/div[@class='specific_letter']//text()") else []
        item[u"信件回复"] = deal_ntr("".join(re_content).strip())
        item[u"处理部门"] = data["clbm"]
        item[u"回复时间"] = html.xpath("(//div[@class='specific_letter_bottom'])[2]/span[2]/text()")[
            0].strip() if html.xpath("(//div[@class='specific_letter_bottom'])[2]/span[2]/text()") else ""
        item[u"满意度"] = deal_ntr(html.xpath("(//div[@class='specific_letter_bottom'])[2]/span[1]/text()")[
                                    0].strip() if html.xpath(
            "(//div[@class='specific_letter_bottom'])[2]/span[1]/text()") else "")
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
