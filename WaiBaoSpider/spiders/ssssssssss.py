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


class SoBookSpider(scrapy.Spider):
    name = "sobook"
    allowed_domains = ['sobooks.net']
    start_urls = ['https://sobooks.net']

    def parse(self, response):
        pass