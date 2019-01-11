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


class SuQianSpider(scrapy.Spider):
    name = "suqian"
    base_url = "http://bbs.suqian.cn/forum.php?mod=forumdisplay&fid=43&page={}"
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
        for i in range(1, 1001):
            # for i in range(1, 5):
            url = self.base_url.format(i)
            yield Request(url, callback=self.parse_list, headers=self.headers)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//tbody[contains(@id,'normalthread')]")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"问政类型"] = info.xpath("./tr/th/span[1]/a/text()")[0].strip() if info.xpath(
                "./tr/th/span[1]/a/text()") else ""
            item[u"来源"] = info.xpath("./tr/td[2]/a/@title")[0].strip() if info.xpath("./tr/td[2]/a/@title") else ""
            item[u"标题"] = info.xpath("./tr/th/a[@class='s xst']/text()")[0].strip() if info.xpath(
                "./tr/th/a[@class='s xst']/text()") else ""
            item[u"作者"] = info.xpath("./tr/td[4]/cite/a/text()")[0].strip() if info.xpath(
                "./tr/td[4]/cite/a/text()") else ""
            if info.xpath("./tr/td[4]/em[2]/span/text()"):
                item[u"时间"] = info.xpath("./tr/td[4]/em[2]/span/text()")[0].strip()
            elif info.xpath("./tr/td[4]/em[2]/span/span/@title"):
                item[u"时间"] = info.xpath("./tr/td[4]/em[2]/span/span/@title")[0].strip()
            else:
                item[u"时间"] = ""
            item[u"回复"] = info.xpath("./tr/td[5]/a/text()")[0].strip() if info.xpath("./tr/td[5]/a/text()") else ""
            item[u"查看"] = info.xpath("./tr/td[5]/em/text()")[0].strip() if info.xpath("./tr/td[5]/em/text()") else ""
            item[u"最后发言"] = info.xpath("./tr/td[6]/cite/a/text()")[0].strip() if info.xpath(
                "./tr/td[6]/cite/a/text()") else ""
            if info.xpath("./tr/td[6]/em[2]/a/text()"):
                item[u"最后发言时间"] = info.xpath("./tr/td[6]/em[2]/a/text()")[0].strip()
            elif info.xpath("./tr/td[6]/em[2]/a/span/@title"):
                item[u"最后发言时间"] = info.xpath("./tr/td[6]/em[2]/a/span/@title")[0].strip()
            else:
                item[u"最后发言时间"] = ""
            item[u"链接"] = info.xpath("./tr/th/a[@class='s xst']/@href")[0].strip() if info.xpath(
                "./tr/th/a[@class='s xst']/@href") else ""
            self.dump_list.process_item(item)
            yield Request(item[u"链接"], callback=self.parse_detail, headers=self.headers,
                          meta={"url": item[u"链接"], "author": item[u"作者"], "lx": item[u"问政类型"]})

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"作者"] = data["author"]
        item[u"标题"] = html.xpath("//h1[@class='ts']/span[@id]/text()")[0].strip() if html.xpath(
            "//h1[@class='ts']/span[@id]/text()") else ""
        item[u"类型"] = data["lx"]
        item[u"发表时间"] = html.xpath("(//div[@class='pti'])[1]/div[@class='authi']/em[@id]//text()") if html.xpath(
            "(//div[@class='pti'])[1]/div[@class='authi']/em[@id]//text()") else []
        item[u"发表时间"] = deal_ntr("".join(item[u"发表时间"]))
        item[u"内容"] = html.xpath("(//td[@class='t_f'])[1]//text()") if html.xpath(
            "(//td[@class='t_f'])[1]//text()") else []
        item[u"内容"] = deal_ntr("".join(item[u"内容"]))
        bumenhf = html.xpath("//div[@class='pstl xs1 cl']")
        if len(bumenhf) > 0:
            huifu_list = []
            for i in bumenhf:
                bumen = i.xpath("./div[1]/a[2]/text()")[0].strip() if i.xpath("./div[1]/a[2]/text()") else ""
                huifu = i.xpath("./div[2]/text()") if i.xpath("./div[2]/text()") else []
                huifu = deal_ntr("".join(huifu))
                hftime = i.xpath("./div[2]/span/text()") if i.xpath("./div[2]/span/text()") else []
                hftime = deal_ntr("".join(hftime))
                the_str = u"部门：{} 回复：{} 回复时间：{}".format(bumen, huifu, hftime)
                huifu_list.append(the_str)
            item[u"部门答复1"] = "".join(huifu_list)
        else:
            item[u"部门答复1"] = ""
        item[u"回复"] = html.xpath("(//td[@class='t_f'])[2]//text()") if html.xpath(
            "(//td[@class='t_f'])[2]//text()") else []
        item[u"回复"] = deal_ntr("".join(item[u"回复"]))
        item[u"回复时间"] = html.xpath("(//div[@class='pti'])[2]/div[@class='authi']/em[@id]//text()") if html.xpath(
            "(//div[@class='pti'])[2]/div[@class='authi']/em[@id]//text()") else []
        item[u"回复时间"] = deal_ntr("".join(item[u"回复时间"]))
        item[u"链接"] = data["url"]
        liucheng = html.xpath("(//div[@id='divdescription'])[1]/div")
        if len(liucheng) > 0:
            liucheng_list = []
            for i in liucheng:
                chuliren = i.xpath("./div[1]/font/text()")[0].strip() if i.xpath("./div[1]/font/text()") else " "
                shijian = i.xpath("./div[2]/font/text()")[0].strip() if i.xpath("./div[2]/font/text()") else " "
                qingkuang = i.xpath("./div[3]/text()")[0].strip() if i.xpath("./div[3]/text()") else " "
                liucheng_str = u"处理人：{} 时间：{} 处理：{}".format(chuliren, shijian, qingkuang)
                liucheng_list.append(liucheng_str)
            item[u"处理流程"] = "".join(liucheng_list)
        else:
            item[u"处理流程"] = ""
        self.dump_detail.process_item(item)
