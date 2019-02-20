# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: hebi.py
# @Software: PyCharm

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class HeBiSpider(scrapy.Spider):
    name = "hebi"
    base_url = "http://www.hebi.gov.cn/eportal/ui?currentPage={}&moduleId=13299&pageId=436795"

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
    form_data = {
        "filter_EQ_MSG_ID": "",
        "filter_LIKE_TITLE": "",
    }

    def start_requests(self):
        for i in range(1, 1828):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield FormRequest(url, callback=self.parse_list, formdata=self.form_data, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='hyxanr2']/tbody/tr")[1:-1]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件编号"] = "'{}'".format(
                info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"类型"] = info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else ""
            item[u"信件标题"] = info.xpath("./td[3]/a/text()")[0].strip() if info.xpath("./td[3]/a/text()") else ""
            item[u"链接"] = "http://www.hebi.gov.cn{}".format(
                info.xpath("./td[3]/a/@href")[0].strip() if info.xpath("./td[3]/a/@href") else "")
            item[u"时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"处理状态"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"姓名"] = html.xpath("(//td[@class='hyxbt hnr'])[1]/text()")[0].strip() if html.xpath(
            "(//td[@class='hyxbt hnr'])[1]/text()") else ""
        item[u"标题"] = html.xpath("(//td[@class='hyxbt hnr'])[2]/text()")[0].strip() if html.xpath(
            "(//td[@class='hyxbt hnr'])[2]/text()") else ""
        content = html.xpath("(//td[@class='hyxbt hnr'])[3]//text()") if html.xpath(
            "(//td[@class='hyxbt hnr'])[3]//text()") else []
        item[u"内容"] = deal_ntr("".join(content))
        item[u"咨询时间"] = html.xpath("(//td[@class='hyxbt hnr'])[4]/div/text()")[0].strip() if html.xpath(
            "(//td[@class='hyxbt hnr'])[4]/div/text()") else ""
        item[u"处理状态"] = html.xpath("(//td[@class='hyxbt hnr'])[5]/div/text()")[0].strip() if html.xpath(
            "(//td[@class='hyxbt hnr'])[5]/div/text()") else ""
        re_content = html.xpath("(//td[@class='hyxbt hnr'])[6]/div//text()") if html.xpath(
            "(//td[@class='hyxbt hnr'])[6]/div//text()") else []
        item[u"回复内容"] = deal_ntr("".join(re_content))
        item[u"处理时间"] = html.xpath("(//td[@class='hyxbt hnr'])[7]/text()")[0].strip() if html.xpath(
            "(//td[@class='hyxbt hnr'])[7]/text()") else ""
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
