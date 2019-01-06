# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class XuzhouSpider(scrapy.Spider):
    name = 'xuzhou'
    base_url = "http://12345.xz.gov.cn/xzbmweb/ywxxtemplate/ggfw_slgs.aspx"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    data_form = {
        "__EVENTARGUMENT": "",
        "CaseGgfwAll1$Pager_input": "",
        "__EVENTTARGET": "CaseGgfwAll1$Pager",
    }

    def start_requests(self):
        for i in range(1, 279):
        # for i in range(1, 2):
            print("page_%s" % str(i))
            self.data_form["__EVENTARGUMENT"] = str(i)
            self.data_form["CaseGgfwAll1$Pager_input"] = str(i - 1)
            yield FormRequest(self.base_url, formdata=self.data_form, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//tr[@class='HeadStyleOfDataGridItemStyle']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = "'{}'".format(
                info.xpath("./td[1]/font/text()")[0].strip() if info.xpath("./td[1]/font/text()") else "")
            item[u"工单号"] = "'{}'".format(
                deal_ntr(info.xpath("./td[2]/font/text()")[0].strip() if info.xpath("./td[2]/font/text()") else ""))
            item[u"标题"] = info.xpath("./td[3]/font/a/text()")[0].strip() if info.xpath("./td[3]/font/a/text()") else ""
            item[u"类型"] = info.xpath("./td[4]/font/text()")[0].strip() if info.xpath("./td[4]/font/text()") else ""
            item[u"办理部门"] = info.xpath("./td[5]/font/text()")[0].strip() if info.xpath("./td[5]/font/text()") else ""
            item[u"办理状态"] = info.xpath("./td[6]/font/text()")[0].strip() if info.xpath("./td[6]/font/text()") else ""
            temp_url = info.xpath("./td[3]/font/a/@onclick")[0].strip() if info.xpath("./td[3]/font/a/@onclick") else ""
            temp_url = re.search('window.open\("\.\.(.*?)"', temp_url)
            if temp_url:
                item[u"链接"] = "http://12345.xz.gov.cn/xzbmweb{}".format(temp_url.group(1))
                yield Request(item[u"链接"], callback=self.parse_detail, meta={"url": item[u"链接"]})
            else:
                print("no url !!!!!!!")
                item[u"链接"] = ""
            self.dump_list.process_item(item)

    def parse_detail(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        data = response.meta
        item = {}
        item[u"标题"] = html.xpath("//span[@id='CaseDetail_lbl_title']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_title']/text()") else ""
        item[u"受理日期"] = html.xpath("//span[@id='CaseDetail_lbl_requestDate']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_requestDate']/text()") else ""
        item[u"内容"] = deal_ntr(html.xpath("//span[@id='CaseDetail_lbl_content']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_content']/text()") else "")
        item[u"问题类型"] = html.xpath("//span[@id='CaseDetail_lbl_CaseType']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_CaseType']/text()") else ""
        item[u"反馈时间"] = html.xpath("//span[@id='CaseDetail_lbl_answerDate']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_answerDate']/text()") else ""
        item[u"回复意见"] = deal_ntr(
            html.xpath("//span[@id='CaseDetail_lbl_AnswerContent']/text()")[0].strip() if html.xpath(
                "//span[@id='CaseDetail_lbl_AnswerContent']/text()") else "")
        item[u"回访结果"] = html.xpath("//span[@id='CaseDetail_lbl_result']/text()")[0].strip() if html.xpath(
            "//span[@id='CaseDetail_lbl_result']/text()") else ""
        bcfk = html.xpath("//span[@id='CaseDetail_lbl_bcfk']//text()") if html.xpath(
            "//span[@id='CaseDetail_lbl_bcfk']/text()") else []
        item[u"补充反馈"] = deal_ntr("".join(bcfk))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
