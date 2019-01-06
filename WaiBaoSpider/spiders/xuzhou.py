# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr
import os


class XuzhouSpider(scrapy.Spider):
    name = 'xuzhou'
    allowed_domains = ['http://12345.xz.gov.cn']
    data_path = os.getcwd() + "/WaiBaoSpider/data/%s/" % name
    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)
    start_urls = ['http://http://12345.xz.gov.cn/']

    def parse(self, response):
        pass
