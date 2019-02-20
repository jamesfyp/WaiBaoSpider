# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import re
import os


class LaiWuSpider(scrapy.Spider):
    name = "laiwu"
    base_purl = "http://www.laiwu.gov.cn/jact/front/dataproxy_mailnewlist.action?startrecord={sid}&endrecord={eid}&perpage=19&groupSize=3"
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
    data_form = {
        "sysid": "1",
        "datadetailid": "null",
        "dicvalue": "null",
        "orderfield": "1",
    }

    def start_requests(self):
        i = 1
        while i < 9177:
            # while i < 2:
            print(i)
            url = self.base_purl.format(sid=i, eid=i + 56)
            i = i + 57
            yield FormRequest(url, headers=self.headers, formdata=self.data_form, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        # print(body)
        result = re.search("\[(.*)\]", body, re.DOTALL).group(1)
        html = etree.HTML(result)
        lines = html.xpath("//tr[@class='tr_css']")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"办件编号"] = "'{}'".format(
                info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else "")
            item[u"标题"] = info.xpath("./td[2]/a/text()")[0].strip() if info.xpath("./td[2]/a/text()") else ""
            item[u"链接"] = "http://www.laiwu.gov.cn/jact/front/{}".format(
                info.xpath("./td[2]/a/@href")[0].strip() if info.xpath("./td[2]/a/@href") else "")
            item[u"处理情况"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"提交时间"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"提交部门"] = info.xpath("./td[5]/a/text()")[0].strip() if info.xpath("./td[5]/a/text()") else ""
            item[u"点击次数"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "bjbh": item[u"办件编号"], "clqk": item[u"处理情况"]})

    def parse_detail(self, response):
        # pass
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"办件标题"] = deal_ntr(
            html.xpath("(//tr[@class='trbg02'])[1]/td[@class='list_pd2']/text()")[0].strip() if html.xpath(
                "(//tr[@class='trbg02'])[1]/td[@class='list_pd2']/text()") else "")
        item[u"内容"] = deal_ntr(
            html.xpath("(//tr[@class='trbg02'])[2]/td[@class='list_pd2']/text()")[0].strip() if html.xpath(
                "(//tr[@class='trbg02'])[2]/td[@class='list_pd2']/text()") else "")
        item[u"附件"] = deal_ntr(
            html.xpath("(//tr[@class='trbg02'])[3]/td[@class='list_pd2']/text()")[0].strip() if html.xpath(
                "(//tr[@class='trbg02'])[3]/td[@class='list_pd2']/text()") else "")
        item[u"办件编号"] = data["bjbh"]
        item[u"提交时间"] = html.xpath("(//tr[@class='trbg02'])[6]/td[@class='list_pd1']/text()")[0].strip().replace(
            u"&nbsp", u"") if html.xpath("(//tr[@class='trbg02'])[6]/td[@class='list_pd1']/text()") else ""
        item[u"处理状态"] = data["clqk"]
        re_content = html.xpath("(//td[@valign='top'])[1]/table[4]/tr[2]/td[2]//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[4]/tr[2]/td[2]//text()") else []
        item[u"答复内容"] = deal_ntr("".join(re_content))
        item[u"答复人"] = html.xpath("(//td[@valign='top'])[1]/table[4]/tr[3]/td[2]/text()")[0].strip() if html.xpath(
            "(//td[@valign='top'])[1]/table[4]/tr[3]/td[2]/text()") else ""
        item[u"答复时间"] = html.xpath("(//td[@valign='top'])[1]/table[4]/tr[3]/td[4]/text()")[0].strip() if html.xpath(
            "(//td[@valign='top'])[1]/table[4]/tr[3]/td[4]/text()") else ""
        fujian2 = html.xpath("(//td[@valign='top'])[1]/table[4]/tr[4]/td[2]//text()") if html.xpath(
            "(//td[@valign='top'])[1]/table[4]/tr[4]/td[2]//text()") else []
        item[u"附件2"] = deal_ntr("".join(fujian2))
        item[u"链接"] = data["url"]
        self.dump_detail.process_item(item)
