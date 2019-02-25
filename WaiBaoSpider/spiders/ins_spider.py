# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/2/24
# @File: ins_spider.py
# @Software: PyCharm

import json
import logging
from urllib import quote
import scrapy
from WaiBaoSpider.ins_spider.get_cookies import getcookies
from scrapy import Request, FormRequest
from lxml import etree
from WaiBaoSpider.utils.csvWriter import CSVDumper
from WaiBaoSpider.utils.base import unicode_body, deal_ntr

class InsSpider(scrapy.Spider):

    name = "insspider"
    base_url = "http://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=%7B%22tag_name%22%3A%22{key_word}%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A8%2C%22after%22%3A%22{after}%22%7D"
    get_user_url = "https://www.instagram.com/graphql/query/?query_hash=292c781d60c07571d58d9ef7808888ef&variables=%7B%22shortcode%22%3A%22{uid}%22%2C%22include_reel%22%3Atrue%2C%22include_logged_out%22%3Afalse%7D"
    start_after = "QVFDU2JuMHBQVG1IdlJnbGZTOGRrdTcyTy1fblA5blJWU2l4cl9yVUN5VnVMOWJ5bW00U190b3Q3V0JIZS1zTU5KSmdJUnFveUxqMGRYM2x1SF93RFNhSw=="
    keyword = "面膜"


    def start_requests(self):
        the_coo = getcookies()
        cookies = {}
        for i in the_coo:
            cookies[i["name"]] = i["value"]
        url = self.base_url.format(key_word=quote(self.keyword), after=quote(self.start_after))
        yield Request(url, callback=self.parse_list, cookies=cookies)

    def parse_list(self, response):
        print(response)