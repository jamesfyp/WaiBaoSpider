# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class LiuAnSpider(scrapy.Spider):
    name = "liuan"
    base_url = "http://www.luan.gov.cn/nocache/supervision/?product_id=3&page={}"
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    dump_list = CSVDumper(data_path + "%s_list.csv" % name)
    dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    # custom_settings = {
    # }

    def start_requests(self):
        for i in range(1, 2160):
            # for i in range(2, 4):
            url = self.base_url.format(i)
            print(url)
            yield Request(url, headers=self.headers, callback=self.parse_list)

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        lines = html.xpath("//table[@class='is-xjnr']/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"类别"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            title = info.xpath("./td[3]/a//text()") if info.xpath("./td[3]/a//text()") else []
            item[u"来信标题"] = deal_ntr("".join(title).strip())
            item[u"来信时间"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"处理状态"] = info.xpath("./td[7]/span/text()")[0].strip() if info.xpath("./td[7]/span/text()") else ""
            item[u"浏览次数"] = info.xpath("./td[9]/text()")[0].strip() if info.xpath("./td[9]/text()") else ""
            item[u"回复评价"] = info.xpath("./td[11]/a/text()")[0].strip() if info.xpath("./td[11]/a/text()") else ""
            item[u"链接"] = "http://www.luan.gov.cn{}".format(
                info.xpath("./td[3]/a/@href")[0].strip() if info.xpath("./td[3]/a/@href") else "")
            if info.xpath("./td[3]/a/span/text()"):
                item[u"是否公开"] = u"不公开"
                item_detail = {
                    u"链接": item[u"链接"],
                    u"标题": item[u"来信标题"],
                    u"来信人": u"",
                    u"来信时间": item[u"来信时间"],
                    u"处理情况": item[u"处理状态"],
                    u"督办部门": u"",
                    u"问题类别": u"",
                    u"浏览": item[u"浏览次数"],
                    u"来信内容": u"",
                    u"回复内容": u"",
                    u"回复单位": u"",
                    u"回复时间": u"",
                    u"是否公开": u"否",
                }
                self.dump_detail.process_item(item_detail)
            else:
                item[u"是否公开"] = u"公开"
                yield Request(item[u"链接"], headers=self.headers, callback=self.parse_detail,
                              meta={"url": item[u"链接"], "llcs": item[u"浏览次数"], "clzt": item[u"处理状态"]})
            self.dump_list.process_item(item)

    def parse_detail(self, response):
        body = unicode_body(response)
        data = response.meta
        html = etree.HTML(body)
        item = {}
        item[u"链接"] = data["url"]
        item[u"标题"] = html.xpath("//div[@class='is-newstitle']/text()")[0].strip() if html.xpath(
            "//div[@class='is-newstitle']/text()") else ""
        item[u"来信人"] = html.xpath("//div[@class='is-mailinfo']/text()[1]")[0].strip().replace(u"来信人：",
                                                                                              u"") if html.xpath(
            "//div[@class='is-mailinfo']/text()[1]") else ""
        item[u"来信时间"] = html.xpath("//div[@class='is-mailinfo']/text()[2]")[0].strip().replace(u"来信时间：",
                                                                                               u"") if html.xpath(
            "//div[@class='is-mailinfo']/text()[2]") else ""
        item[u"处理情况"] = data["clzt"]
        dbbm = html.xpath("//div[@class='is-mailinfo']/span[4]/text()[1]")[0].strip().replace(u"|",
                                                                                              u"").replace(
            u"督办部门：", u"") if html.xpath("//div[@class='is-mailinfo']/span[4]/text()[1]") else ""
        item[u"督办部门"] = deal_ntr(dbbm)
        item[u"问题类别"] = html.xpath("//div[@class='is-mailinfo']/span[4]/span[@class='red'][1]/text()")[
            0].strip() if html.xpath("//div[@class='is-mailinfo']/span[4]/span[@class='red'][1]/text()") else ""
        item[u"浏览"] = data["llcs"]
        lxnr = html.xpath("//div[@class='is-mailwen']/p//text()") if html.xpath(
            "//div[@class='is-mailwen']/p//text()") else []
        item[u"来信内容"] = deal_ntr("".join(lxnr))
        hf_content = html.xpath("//div[@class='is-hfcontent']//text()") if html.xpath(
            "//div[@class='is-hfcontent']//text()") else []
        item[u"回复内容"] = deal_ntr("".join(hf_content))
        item[u"回复单位"] = html.xpath("//div[@class='is-mialhf']/h1/span[2]/text()")[0].strip().replace(u"回复单位：",
                                                                                                     u"") if html.xpath(
            "//div[@class='is-mialhf']/h1/span[2]/text()") else ""
        item[u"回复时间"] = html.xpath("//div[@class='is-mialhf']/h1/span[1]/text()")[0].strip().replace(u"回复时间：",
                                                                                                     u"") if html.xpath(
            "//div[@class='is-mialhf']/h1/span[1]/text()") else ""
        item[u"是否公开"] = u"是"
        self.dump_detail.process_item(item)
