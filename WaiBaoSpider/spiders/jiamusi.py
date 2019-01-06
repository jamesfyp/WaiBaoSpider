# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class DalianSpider(scrapy.Spider):
    name = 'jiamusi'
    base_list_url1 = "http://www.jms.gov.cn/html/zmhd/page/jms_10030002_{}.html"
    base_list_url2 = "http://www.jms.gov.cn/html/zmhd/page/jms_10030001_{}.html"
    data_path = os.getcwd() + "/WaiBaoSpider/data/jiamusi/"
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)

    def start_requests(self):
        for i in range(1, 150):
            url = self.base_list_url1.format(i)
            print(url)
            yield Request(url, callback=self.parse_list, meta={"source": u"反映问题"})
        for i in range(1, 145):
            url = self.base_list_url2.format(i)
            print(url)
            yield Request(url, callback=self.parse_list, meta={"source": u"咨询问题"})

    def parse_list(self, response):
        body = unicode_body(response)
        source = response.meta["source"]
        html = etree.HTML(body)
        lines = html.xpath("//ul[@id='wszxList']/li")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"来源"] = source
            item[u"标题"] = info.xpath("./span[1]/a/text()")[0].strip() if info.xpath("./span[1]/a/text()") else ""
            item[u"链接"] = "http://www.jms.gov.cn{}".format(
                info.xpath("./span[1]/a/@href")[0] if info.xpath("./span[1]/a/@href") else "")
            item[u"类型"] = info.xpath("./span[2]/text()")[0].strip() if info.xpath("./span[2]/text()") else ""
            item[u"答复部门"] = info.xpath("./span[3]/text()")[0].strip() if info.xpath("./span[3]/text()") else ""
            item[u"状态"] = info.xpath("./span[4]/text()")[0].strip() if info.xpath("./span[4]/text()") else ""
            item[u"发布时间"] = info.xpath("./span[5]/text()")[0].strip() if info.xpath("./span[5]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, meta={"url": item[u"链接"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"来信人"] = html.xpath("//span[@id='releaseMan']/text()")[0].strip() if html.xpath(
            "//span[@id='releaseMan']/text()") else ""
        item[u"咨询时间"] = html.xpath("//span[@id='zxsj']/text()")[0].strip() if html.xpath(
            "//span[@id='zxsj']/text()") else ""
        item[u"信件标题"] = html.xpath("//span[@id='title']/text()")[0].strip() if html.xpath(
            "//span[@id='title']/text()") else ""
        item[u"所属类型"] = html.xpath("//span[@id='conType']/text()")[0].strip() if html.xpath(
            "//span[@id='conType']/text()") else ""
        item[u"处理情况"] = html.xpath("//span[@id='state']/text()")[0].strip() if html.xpath(
            "//span[@id='state']/text()") else ""
        item[u"信件内容"] = deal_ntr(
            html.xpath("//span[@id='content']/text()")[0].strip() if html.xpath("//span[@id='content']/text()") else "")
        fujian = html.xpath("//span[@id='accessory']//text()") if html.xpath("//span[@id='accessory']//text()") else []
        item[u"附件"] = deal_ntr("".join(fujian).strip())
        item[u"承办单位"] = html.xpath("//span[@id='conDept']/text()")[0].strip() if html.xpath(
            "//span[@id='conDept']/text()") else ""
        item[u"处理时间"] = html.xpath("//span[@id='replyTime']/text()")[0].strip() if html.xpath(
            "//span[@id='replyTime']/text()") else ""
        item[u"处理结果"] = deal_ntr(html.xpath("//span[@id='replyContent']/text()")[0].strip() if html.xpath(
            "//span[@id='replyContent']/text()") else "")
        hfmyd = html.xpath("//div[@id='myd']//text()") if html.xpath("//div[@id='myd']//text()") else []
        hfmyd = deal_ntr("".join(hfmyd))
        if hfmyd:
            item[u"回复满意度"] = hfmyd
        else:
            item[u"回复满意度"] = u"用户暂无评价"
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
