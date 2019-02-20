# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class XuanChengSpider(scrapy.Spider):
    name = "xuancheng"
    base_url = "http://www.xuancheng.gov.cn/supervision/productList/product_id=3/page-{}/"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for i in range(1, 1416):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='letter_list_box']/ul/li")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"信件编号"] = "'{}'".format(info.xpath("./p[1]/text()")[0].strip() if info.xpath("./p[1]/text()") else "")
            item[u"处理部门"] = info.xpath("./p[2]/text()")[0].strip() if info.xpath("./p[2]/text()") else ""
            item[u"来信标题"] = info.xpath("./p[3]/a/text()")[0].strip() if info.xpath("./p[3]/a/text()") else ""
            item[u"链接"] = "http://www.xuancheng.gov.cn{}".format(
                info.xpath("./p[3]/a/@href")[0].strip() if info.xpath("./p[3]/a/@href") else "")
            item[u"来信时间"] = info.xpath("./p[4]/text()")[0].strip() if info.xpath("./p[4]/text()") else ""
            item[u"审核时间"] = info.xpath("./p[5]/text()")[0].strip() if info.xpath("./p[5]/text()") else ""
            item[u"处理状态"] = info.xpath("./p[6]/font/text()")[0].strip() if info.xpath("./p[6]/font/text()") else ""
            item[u"浏览次数"] = info.xpath("./p[7]/text()")[0].strip() if info.xpath("./p[7]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "lxsj": item[u"来信时间"], "shsj": item[u"审核时间"],
                                "cjzt": item[u"处理状态"], "llcs": item[u"浏览次数"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"1标题"] = html.xpath("//div[@class='detail_letter_box']/table/thead/tr/td/p/text()")[
            0].strip() if html.xpath("//div[@class='detail_letter_box']/table/thead/tr/td/p/text()") else ""
        item[u"2来信人"] = html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[1]/td[2]/div/text()")[
            0].strip() if html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[1]/td[2]/div/text()") else ""
        item[u"3处理情况"] = data["cjzt"]
        item[u"4浏览"] = data["llcs"]
        item[u"5问政时间"] = data["lxsj"]
        item[u"6审核时间"] = data["shsj"]
        item[u"7受理时间"] = html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[2]/td[6]/div/text()")[
            0].strip() if html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[2]/td[6]/div/text()") else ""
        content = html.xpath(
            "//div[@class='detail_letter_box']/table/tbody/tr[3]//div[@class='letter_nr']//text()") if html.xpath(
            "//div[@class='detail_letter_box']/table/tbody/tr[3]//div[@class='letter_nr']//text()") else []
        item[u"8内容"] = deal_ntr("".join(content))
        tr4 = html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[1]//text()") if html.xpath(
            "//div[@class='detail_letter_box']/table/tbody/tr[4]/td[1]//text()") else []
        tr4 = "".join(tr4).strip()
        if u"回复单位：" in tr4:
            item[u"a回复单位"] = html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[2]/div/text()")[
                0].strip() if html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[2]/div/text()") else ""
            item[u"b回复时间"] = html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[4]/div/text()")[
                0].strip() if html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[4]/div/text()") else ""
            re_content = html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[5]//div[@class='letter_nr']//text()") if html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[5]//div[@class='letter_nr']//text()") else []
            item[u"c回复内容"] = deal_ntr("".join(re_content))
            item[u"d评价"] = deal_ntr(
                html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[6]//div[@class='letter_nr']//text()")[
                    0].strip() if html.xpath(
                    "//div[@class='detail_letter_box']/table/tbody/tr[6]//div[@class='letter_nr']//text()") else "")
        elif u"回复：" in tr4:
            item[u"a回复单位"] = u""
            item[u"b回复时间"] = u""
            item[u"c回复内容"] = deal_ntr(
                html.xpath("//div[@class='detail_letter_box']/table/tbody/tr[4]/td[2]/div/text()")[
                    0].strip() if html.xpath(
                    "//div[@class='detail_letter_box']/table/tbody/tr[4]/td[2]/div/text()") else "")
            item[u"d评价"] = u""
        elif u"价问贴为：" in tr4:
            item[u"a回复单位"] = u""
            item[u"b回复时间"] = u""
            re_con = html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[5]//div[@class='letter_nr']//text()") if html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[5]//div[@class='letter_nr']//text()") else []
            item[u"c回复内容"] = deal_ntr("".join(re_con))
            pingjia = html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[4]//div[@class='letter_nr']//text()") if html.xpath(
                "//div[@class='detail_letter_box']/table/tbody/tr[4]//div[@class='letter_nr']//text()") else []
            item[u"d评价"] = deal_ntr("".join(pingjia))
        else:
            item[u"a回复单位"] = u""
            item[u"b回复时间"] = u""
            item[u"c回复内容"] = u""
            item[u"d评价"] = u""
        item[u"9链接"] = data["url"]
        self.dump_detail.process_item(item)
