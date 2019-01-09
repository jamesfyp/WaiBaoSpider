# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class ChengDuSpider(scrapy.Spider):
    name = "chengdu"
    base_url = "http://12345.chengdu.gov.cn/openWorkList?page={}"
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
    data_form = {
        "pageID": "",
    }

    def start_requests(self):
        for i in range(1964, 2949):
            # for i in range(1, 2):
            self.data_form["pageID"] = str(i)
            url = self.base_url.format(i)
            yield FormRequest(url, callback=self.parse_list, formdata=self.data_form, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='left5']/ul/li")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"标题"] = info.xpath("./a/div[1]/text()")[0].strip() if info.xpath("./a/div[1]/text()") else ""
            item[u"链接"] = "http://12345.chengdu.gov.cn/{}".format(
                info.xpath("./a/@href")[0].strip() if info.xpath("./a/@href") else "")
            item[u"办理单位"] = info.xpath("./a/div[3]/text()")[0].strip() if info.xpath("./a/div[3]/text()") else ""
            item[u"类别"] = info.xpath("./a/div[4]/text()")[0].strip() if info.xpath("./a/div[4]/text()") else ""
            item[u"访问量"] = info.xpath("./a/div[5]/text()")[0].strip() if info.xpath("./a/div[5]/text()") else ""
            item[u"时间"] = info.xpath("./a/div[6]/text()")[0].strip() if info.xpath("./a/div[6]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"来信标题"] = html.xpath("//table[@class='tb']/tbody/tr[2]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='tb']/tbody/tr[2]/td[2]/text()") else ""
        item[u"来信时间"] = html.xpath("//table[@class='tb']/tbody/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='tb']/tbody/tr[3]/td[2]/text()") else ""
        item[u"来信内容"] = deal_ntr(html.xpath("//table[@class='tb']/tbody/tr[4]/td[2]/text()")[0].strip() if html.xpath(
            "//table[@class='tb']/tbody/tr[4]/td[2]/text()") else "")
        clbu_clsj = html.xpath("//table[@class='tb']/tbody/tr")[7:-2]
        big_str = ""
        for i in clbu_clsj:
            the_str = i.xpath("./td//text()") if i.xpath("./td//text()") else []
            the_str = "_".join(the_str)
            big_str = big_str + the_str + "_"
        item[u"办理情况"] = big_str
        bljg = html.xpath("//table[@class='tb']/tbody/tr")[-1]
        bljg = bljg.xpath(".//text()") if bljg.xpath(".//text()") else []
        item[u"办理结果"] = deal_ntr("".join(bljg))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
