# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body


class TestProject(scrapy.Spider):
    name = "testp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36",
    }

    def start_requests(self):
        url = "https://weibo.com/1761616742/HlQcT57wD?refer_flag=1001030103_"
        yield Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        print(response.url)
