# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
"""
.net
"""
import re

import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class NeiJiangSpider(scrapy.Spider):
    name = "neijiang"
    base_url = "http://www.njwlwz.gov.cn/Mail/Allemail.aspx?MailBox=%u6240%u6709%u4fe1%u7bb1&Manager=%25&ShowTitle=1&MailType=%25&Title=%25&Sender=%25&Open=1"
    data_path = os.getcwd() + "/WaiBaoSpider/data/"
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    i = 1

    def start_requests(self):
        url = self.base_url
        yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='SearchPanel']//table[@class='GridView']/tr")[1:-1]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"类别"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"时间"] = info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else ""
            item[u"标题"] = info.xpath("./td[4]/a/text()")[0].strip() if info.xpath("./td[4]/a/text()") else ""
            item[u"发送人"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"接收人"] = info.xpath("./td[6]/a/text()")[0].strip() if info.xpath("./td[6]/a/text()") else ""
            item[u"回复人"] = info.xpath("./td[7]/text()")[0].strip() if info.xpath("./td[7]/text()") else ""
            item[u"状态"] = info.xpath("./td[8]/text()")[0].strip() if info.xpath("./td[8]/text()") else ""
            link = info.xpath("./td[4]/a/@href")[0].strip() if info.xpath("./td[4]/a/@href") else ""
            id = re.search(u"=(\d+)", link).group(1)
            item[u"链接"] = "http://www.njwlwz.gov.cn/MailBox_SZ.aspx?Mode=View&id={}".format(id)
            url = "http://www.njwlwz.gov.cn/Mail/Allemail_Show.aspx?MailBox=%CA%D0%B3%A4%D0%C5%CF%E4&ShowTitle=1&ID={}".format(
                id)
            self.dump_list.process_item(item)
            yield Request(url, callback=self.parse_detail, headers=self.headers, meta={"url": item[u"链接"]})
        data_form = {
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$SmailSearch1$GridView1$ctl23$LinkButtonNextPage",
            "__VIEWSTATE": "",
            "__VIEWSTATEGENERATOR": "",
            "__EVENTVALIDATION": "",
            "ctl00$ContentPlaceHolder1$SmailSearch1$GridView1$ctl23$txtNewPageIndex": "",
            "ctl00_ContentPlaceHolder1_ToolBar1_CheckedItems": "",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTARGUMENT": "",
            "ctl00$ContentPlaceHolder1$SmailSearch1$HF_PageIndex": "1",
            "ctl00_ContentPlaceHolder1_ToolBar1_Properties": "%3Cr%3E%3Cc%3E%3Cr%3E%3Cc%3EApplicationPath%3C%2Fc%3E%3Cc%3E%2F%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EAutoPostBackOnCheckChanged%3C%2Fc%3E%3Cc%3Efalse%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EAutoPostBackOnSelect%3C%2Fc%3E%3Cc%3Etrue%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EClientEvents%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EClientInitCondition%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EClientRenderCondition%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EClientTemplates%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EControlId%3C%2Fc%3E%3Cc%3Ectl00%24ContentPlaceHolder1%24ToolBar1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3ECssClass%3C%2Fc%3E%3Cc%3E%E6%A0%87%E9%A2%98%E5%B7%A5%E5%85%B7%E6%A0%8F%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3ECustomContentIdMap%3C%2Fc%3E%3Cc%3E%5Bobject%20Object%5D%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDropDownIdMap%3C%2Fc%3E%3Cc%3E%5Bobject%20Object%5D%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemActiveCssClass%3C%2Fc%3E%3Cc%3EitemActive%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemCheckedActiveCssClass%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemCheckedCssClass%3C%2Fc%3E%3Cc%3EitemChecked%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemCheckedHoverCssClass%3C%2Fc%3E%3Cc%3EitemActive%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemCssClass%3C%2Fc%3E%3Cc%3Eitem%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemDisabledCheckedCssClass%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemDisabledCssClass%3C%2Fc%3E%3Cc%3EitemDisabled%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemDropDownImageHeight%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemDropDownImagePosition%3C%2Fc%3E%3Cc%3E1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemDropDownImageWidth%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemExpandedCssClass%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemHeight%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemHoverCssClass%3C%2Fc%3E%3Cc%3EitemHover%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemImageHeight%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemImageWidth%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemTextImageRelation%3C%2Fc%3E%3Cc%3E1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemTextImageSpacing%3C%2Fc%3E%3Cc%3E5%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EDefaultItemWidth%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EEnabled%3C%2Fc%3E%3Cc%3Etrue%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EItemSpacing%3C%2Fc%3E%3Cc%3E1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EImagesBaseUrl%3C%2Fc%3E%3Cc%3E%2Fimages%2F%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EHeight%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EOrientation%3C%2Fc%3E%3Cc%3E1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EPlaceHolderId%3C%2Fc%3E%3Cc%3Ectl00_ContentPlaceHolder1_ToolBar1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EUseFadeEffect%3C%2Fc%3E%3Cc%3Etrue%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EWebService%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EWebServiceCustomParameter%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EWebServiceMethod%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3EWidth%3C%2Fc%3E%3Cc%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3C%2Fr%3E",
            "ctl00_ContentPlaceHolder1_ToolBar1_ItemStorage": "%3Cr%3E%3Cc%3E%3Cr%3E%3Cc%3E%3Cr%3E%3Cc%3E31%3C%2Fc%3E%3Cc%3Ep_Cancel%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E36%3C%2Fc%3E%3Cc%3E5%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E10%3C%2Fc%3E%3Cc%3Ehistory.back()%3B%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E28%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E25%3C%2Fc%3E%3Cc%3ECancel%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E45%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E48%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E27%3C%2Fc%3E%3Cc%3Ecancel.ico%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E52%3C%2Fc%3E%3Cc%3E1%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E26%3C%2Fc%3E%3Cc%3E16%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3Cc%3E%3Cr%3E%3Cc%3E33%3C%2Fc%3E%3Cc%3E%E8%BF%94%E5%9B%9E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3C%2Fr%3E%3C%2Fc%3E%3C%2Fr%3E",
        }
        input_list = html.xpath("//form[@name='aspnetForm']/div/input")
        for ele in input_list:
            name = ele.xpath("./@name")[0].strip()
            if name == "__VIEWSTATE":
                a = ele.xpath("./@value")[0].strip()
                data_form["__VIEWSTATE"] = a
            elif name == "__VIEWSTATEGENERATOR":
                data_form["__VIEWSTATEGENERATOR"] = ele.xpath("./@value")[0]
            elif name == "__EVENTVALIDATION":
                data_form["__EVENTVALIDATION"] = ele.xpath("./@value")[0]
        yield FormRequest(self.base_url, formdata=data_form, headers=self.headers, callback=self.parse_list)
        print("list_page>>>>>: {}".format(self.i))
        self.i += 1

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"标题"] = html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_Title']/text()")[
            0].strip() if html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_Title']/text()") else ""
        item[u"来信人"] = \
            html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_UserName']/text()")[
                0].strip() if html.xpath(
                "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_UserName']/text()") else ""
        item[u"来信时间"] = \
            html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_AddDate']/text()")[
                0].strip() if html.xpath(
                "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_AddDate']/text()") else ""
        item[u"状态"] = html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label9']/text()")[
            0].strip() if html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label9']/text()") else ""
        item[u"来信内容"] = html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_Content']//text()") if html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_DetailsView1_Label_Content']//text()") else []
        item[u"来信内容"] = deal_ntr("".join(item[u"来信内容"]))
        item[u"回复单位"] = \
            html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label_UserName']/text()")[
                0].strip() if html.xpath(
                "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label_UserName']/text()") else ""
        item[u"回复时间"] = html.xpath("//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label3']/text()")[
            0].strip() if html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label3']/text()") else ""
        item[u"回复内容"] = html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label_AnswerContent']//text()") if html.xpath(
            "//span[@id='ctl00_ContentPlaceHolder1_MailShow1_GridView1_ctl02_Label_AnswerContent']//text()") else []
        item[u"回复内容"] = deal_ntr("".join(item[u"回复内容"]))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
