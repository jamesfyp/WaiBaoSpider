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


class ZhaoQingSpider(scrapy.Spider):
    name = "zhaoqing"
    base_url = "http://wz.zhaoqing.gov.cn/wzpt/index.php?act=political&op=political_list1&curpage={}"
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
        # for i in range(1, 562):
        for i in range(1, 2):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//div[@class='ask_con_right_conall']/table/tbody/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"链接"] = "http://wz.zhaoqing.gov.cn/wzpt/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            item[u"发布账号"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"浏览数"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"评论数"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"发布时间"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"牵头部门"] = info.xpath("./td[7]/a/text()")[0].strip() if info.xpath("./td[7]/a/text()") else ""
            item[u"状态"] = info.xpath("./td[8]/text()")[0].strip() if info.xpath("./td[8]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "fbzh": item[u"发布账号"], "lls": item[u"浏览数"], "zt": item[u"状态"],
                                "title": item[u"标题"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"链接"] = data["url"]
        fyr_zw = html.xpath("//div[@class='ask_department_left']/table/tbody/tr[1]/td")[1:] if len(
            html.xpath("//div[@class='ask_department_left']/table/tbody/tr[1]/td")) > 1 else []
        item[u"发言人及职位"] = deal_ntr("".join(fyr_zw))
        lianxiren = html.xpath("//div[@class='ask_department_left']/table/tbody/tr[2]/td")[1:] if len(
            html.xpath("//div[@class='ask_department_left']/table/tbody/tr[2]/td")) > 1 else []
        item[u"联系人"] = deal_ntr("".join(lianxiren))
        item[u"发言单位"] = html.xpath("//div[@class='ask_department_name']/span/text()")[0].strip() if html.xpath(
            "//div[@class='ask_department_name']/span/text()") else ""
        dwjj = html.xpath("//div[@class='ask_department_con']//text()") if html.xpath(
            "//div[@class='ask_department_con']//text()") else []
        item[u"单位简介"] = deal_ntr("".join(dwjj))
        item[u"标题"] = data["title"]
        item[u"网民"] = data["fbzh"]
        item[u"发布时间"] = html.xpath("//div[@class='liuyan_user_mation']/font[2]/text()")[0].strip() if html.xpath(
            "//div[@class='liuyan_user_mation']/font[2]/text()") else ""
        item[u"浏览记录"] = data["lls"]
        item[u"问政内容"] = html.xpath("(//div[@class='liuyan_user_text'])[1]//text()") if html.xpath("(//div[@class='liuyan_user_text'])[1]//text()") else []
        item[u"部门回复内容"] = html.xpath("")[0].strip() if html.xpath("") else ""
        item[u"回复时间"] = html.xpath("")[0].strip() if html.xpath("") else ""
        item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
        item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
        item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
        item[u""] = html.xpath("")[0].strip() if html.xpath("") else ""
        self.dump_detail.process_item(item)
