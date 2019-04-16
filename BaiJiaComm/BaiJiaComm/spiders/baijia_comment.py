# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/1/7
# @File: base.py
# @Software: PyCharm
import hashlib
import re
import json

import logging

from ..items import BaijiacommItem
from ..utils.db_model import query_author_sql
from scrapy import Request, Spider

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sql = "select `url` from url_table;"

comm_headers = {
    'Host': 'ext.baidu.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'com.baidu.searchbox',
    'Cookie': 'BAIDUID=A83AB4B181022208DB3FA8A3543A1123:FG=1; PSTM=1554859490; BIDUPSID=1E31D60E65BCA898B6739130798550DB; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_BOXFO=_a2OiguO-zG8C; locale=zh; delPer=0; H_PS_PSSID=26524_1436_21089_28767_28723_28558_28838_28585_28603_28625_22159; PSINO=3; __bsi=10207682954277790582_00_67_N_R_47_0303_c02f_Y'
}


def unicode_body(response):
    if isinstance(response.body, unicode):
        return response.body
    try:
        return response.body_as_unicode()
    except:
        try:
            return response.body.decode(response.encoding)
        except:
            raise Exception("Cannot convert response body to unicode!")


class BaiJiaCommSpider(Spider):
    name = "baijiacomm"
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        "ITEM_PIPELINES": {
            "BaiJiaComm.pipelines.BaijiacommPipeline": 100,
        },
        "EXTENSIONS": {
            'scrapy.telnet.TelnetConsole': None,
        }
    }
    # all_urls = [row[0] for row in query_author_sql(sql) if row[0]]
    all_urls = [
        "https://mbd.baidu.com/newspage/data/landingshare?context=%7B%22nid%22%3A%22news_9445884495414432080%22%2C%22sourceFrom%22%3A%22bjh%22%2C%22url_data%22%3A%22bjhauthor%22%7D",
    ]
    comm_base_url = "https://ext.baidu.com/api/comment/v1/comment/getlist?appid=101&sid=t7&cuid=&isInf=1&start={}&num=20&use_uk=1&use_list=1&is_need_at=1&order=12&thread_id={}"

    def start_requests(self):
        for url in self.all_urls:
            logger.info("start this url: %s" % url)
            yield Request(url, callback=self.parse_tid)

    def parse_tid(self, response):
        body = unicode_body(response)
        tid = re.search("\"thread_id\":\"(\d+)?\"", body).group(1)
        page = 0
        if tid:
            comm_url = self.comm_base_url.format(page, tid)
            yield Request(comm_url, headers=comm_headers, callback=self.parse_comm, meta={"pg": page, "tid": tid})

    def parse_comm(self, response):
        page = response.meta["pg"]
        tid = response.meta["tid"]
        body = json.loads(unicode_body(response))
        comm_len = 0
        data_list = body['ret']['list']
        comm_len += len(data_list)
        for data in data_list:
            b_item = BaijiacommItem()
            # mt = int(time.time())
            # para = 'xxx' + 'xxx.com' + str(mt)
            # sign = hashlib.md5(para.encode(encoding='UTF-8')).hexdigest()
            b_item["nickname"] = data['uname']
            b_item["cover"] = data['avatar']
            b_item["comment"] = data['content']
            b_item["comment_time"] = data['create_time']
            # b_item["fabulous"] = data['like_count']
            yield b_item
            reply_comment = data['reply_list']
            if reply_comment:
                comm_len += len(reply_comment)
                for info in reply_comment:
                    item = BaijiacommItem()
                    item["comment"] = info['content']
                    item["comment_time"] = info['create_time']
                    # item["fabulous"] = info['like_count']
                    item["nickname"] = info['uname']
                    item["cover"] = info['avatar']
                    yield item
        if comm_len >= 20 and page < 200:
            page += 20
            next_url = self.comm_base_url.format(page, tid)
            yield Request(next_url, callback=self.parse_comm, meta={"pg": page, "tid": tid})
