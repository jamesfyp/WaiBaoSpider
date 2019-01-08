# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class JieYangSpider(scrapy.Spider):
    name = "jieyang"
    base_url = "http://xfw.jieyang.gov.cn/List.aspx?action=alxd&pageindex={}"
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
        for i in range(1, 47):
            # for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='alxd-tb']/table/tr")[1:]
        print(len(lines))
        for info in lines:
            item = {}
            item[u"编号"] = "'{}'".format(
                info.xpath("./td[1]/a/text()")[0].strip() if info.xpath("./td[1]/a/text()") else "")
            item[u"标题"] = info.xpath("./td[2]/div/a/text()")[0].strip() if info.xpath("./td[2]/div/a/text()") else ""
            item[u"链接"] = "http://xfw.jieyang.gov.cn/{}".format(
                info.xpath("./td[1]/a/@href")[0].strip() if info.xpath("./td[1]/a/@href") else "")
            item[u"提交时间"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            self.dump_list.process_item(item)
            detail_url = item[u"链接"].replace(u"Communication.aspx", u"CommunicationShow.aspx").replace(u"&spetttbb=",
                                                                                                       u"&strqqkkk=").replace(
                u"?action=alxd&", u"?&")
            yield Request(detail_url, callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "xjbh": item[u"编号"], "tjsj": item[u"提交时间"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"信件编号"] = data["xjbh"]
        item[u"提交人"] = html.xpath("//table[@class='lxck-tb']/tr[1]/td[4]/text()")[0].strip() if html.xpath(
            "//table[@class='lxck-tb']/tr[1]/td[4]/text()") else ""
        item[u"提交时间"] = data["tjsj"]
        item[u"问题分类"] = html.xpath("//table[@class='lxck-tb']/tr[2]//span[@id='lab_WTLX']/text()")[
            0].strip() if html.xpath("//table[@class='lxck-tb']/tr[2]//span[@id='lab_WTLX']/text()") else ""
        item[u"信访目的"] = html.xpath("//table[@class='lxck-tb']/tr[3]//span[@id='lbl_Purposes']/text()")[
            0].strip() if html.xpath("//table[@class='lxck-tb']/tr[3]//span[@id='lbl_Purposes']/text()") else ""
        item[u"主题"] = html.xpath("//table[@class='lxck-tb']/tr[4]//span[@id='lab_Title']/text()")[
            0].strip() if html.xpath("//table[@class='lxck-tb']/tr[4]//span[@id='lab_Title']/text()") else ""
        item[u"内容"] = deal_ntr(html.xpath("//table[@class='lxck-tb']/tr[5]//span[@id='lab_Content']/text()")[
                                   0].strip() if html.xpath(
            "//table[@class='lxck-tb']/tr[5]//span[@id='lab_Content']/text()") else "")
        item[u"办理单位"] = html.xpath("//table[@class='lxck-tb']/tr[6]//span[@id='lab_BlDepartment']/text()")[
            0].strip() if html.xpath(
            "//table[@class='lxck-tb']/tr[6]//span[@id='lab_BlDepartment']/text()") else ""
        item[u"回复时间"] = html.xpath("//table[@class='lxck-tb']/tr[6]//span[@id='lab_ReturnTime']/text()")[
            0].strip() if html.xpath("//table[@class='lxck-tb']/tr[6]//span[@id='lab_ReturnTime']/text()") else ""
        item[u"回复内容"] = deal_ntr(
            html.xpath("//table[@class='lxck-tb']/tr[7]//span[@id='lab_ReplyContent']/text()")[
                0].strip() if html.xpath(
                "//table[@class='lxck-tb']/tr[7]//span[@id='lab_ReplyContent']/text()") else "")
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
