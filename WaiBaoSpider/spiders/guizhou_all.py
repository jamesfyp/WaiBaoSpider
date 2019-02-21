# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm

import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body


class GuiZhouSSpider(scrapy.Spider):
    name = "guizhouall"
    # all_list = [
    #     "zhongshanqu-132-15000",
    #     "huichuanqu-27-15000",
    #     "bozhouqu-28-15000",
    #     "tongziqu-29-15000",
    #     "suiyang-30-15000",
    #     "zhengan-31-15000",
    #     "wuchuan-33-15000",
    #     "yuqing-202-16089",
    #     "xishui-37-15000",
    #     "chishui-38-15000",
    #     "renhuai-39-15000",
    #     "xinpuxin-127-15000",
    #     "zhenning-136-15000",
    #     "ziyun-138-15000",
    #     "anshunkaifa-139-15000",
    #     "dafang-142-15000",
    #     "qianxixian-143-15000",
    # ]
    all_list = [
        "zhijin-145-15000",
        "nayong-146-15000",
        "weining-147-15000",
        "hezhang-148-15000",
        "songtao-153-15000",
        "yuping-154-15000",
        "jiangkou-155-15000",
        "shiqianxian-156-16089",
        "yinjiang-157-15000",
        "dejiang-159-16139",
        "yanhe-160-13545",
        "xingyi-191-15000",
        "xingren-192-15000",
        "zhenfeng-194-15000",
        "puan-197-15573",
        "qinglong-195-15000",
        "ceheng-196-15000",
        "kaili-161-15000",
        # "shibing-163-15000",
        # "sansui-164-15000",
        # "zhenyuan-165-15000",
        # "cengong-166-15000",
        # "tianzhu-167-15000",
        # "jinping-168-15247",
        # "taijiang-170-15264",
        # "rongjiang-172-15000",
        # "congjiang-173-15000",
        # "danzhaixian-176-13501",
        # "kailikaifa-177-15000",
        # "fuquan-179-15000",
        # "wengan-180-15000",
        # "huishui-183-8851",
        # "changshun-184-15000",
        # "dushan-185-15000",
        # "sandu-186-15000",
        # "libo-187-15000",
        # "pingtang-188-15000",
    ]
    base_url = "http://www.gzegn.gov.cn/gzszwfww/cxsx/showcxlb.do?pageno={}&applyStartDate=2013-01-01&webId={}"
    # dump_detail = CSVDumper(data_path + "%s_detail.csv" % name)
    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    def start_requests(self):
        for info in self.all_list:
            info_l = info.split("-")
            iname = info_l[0]
            the_id = info_l[1]
            all_page = info_l[2]
            dumper = CSVDumper("%s_list.csv" % iname)
            for i in range(1, int(all_page)):
                print("%s-%s" % (iname, i))
                # for i in range(1, 2):
                # self.data_form["pageID"] = str(i)
                url = self.base_url.format(i, the_id)
                yield Request(url, callback=self.parse_list, headers=self.headers, meta={"dump": dumper})

    def parse_list(self, response):
        body = unicode_body(response)
        html = etree.HTML(body)
        dumper = response.meta["dump"]
        lines = html.xpath("//div[@class='sec']/table/div[@id='tab1_link']/tr")
        print(len(lines))
        for info in lines:
            item = {}
            item[u"序号"] = info.xpath("./td[1]/text()")[0].strip() if info.xpath("./td[1]/text()") else ""
            item[u"链接"] = info.xpath("./td[9]/a/@href")[0].strip() if info.xpath("./td[9]/a/@href") else ""
            item[u"办理编号"] = "'{}'".format(
                info.xpath("./td[2]/text()")[0].strip() if info.xpath("./td[2]/text()") else "")
            item[u"受理部门"] = info.xpath("./td[3]/text()")[0].strip() if info.xpath("./td[3]/text()") else ""
            item[u"受理事项"] = info.xpath("./td[4]/text()")[0].strip() if info.xpath("./td[4]/text()") else ""
            item[u"办理环节"] = info.xpath("./td[5]/text()")[0].strip() if info.xpath("./td[5]/text()") else ""
            item[u"申请日期"] = info.xpath("./td[6]/text()")[0].strip() if info.xpath("./td[6]/text()") else ""
            item[u"办结日期"] = info.xpath("./td[7]/text()")[0].strip() if info.xpath("./td[7]/text()") else ""
            item[u"申请人"] = info.xpath("./td[8]/text()")[0].strip() if info.xpath("./td[8]/text()") else ""
            item[u"办理结果"] = info.xpath("./td[9]/a/text()")[0].strip() if info.xpath("./td[9]/a/text()") else ""
            dumper.process_item(item)
