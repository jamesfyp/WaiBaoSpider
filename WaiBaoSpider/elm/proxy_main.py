# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/23
# @File: proxy_main.py
# @Software: PyCharm

from support import deal_text
from mitmproxy import ctx


# ref_uel = "https://www.ele.me/shop/{}"
# caidan_url = "https://www.ele.me/restapi/shopping/v2/menu?restaurant_id={}"

# headers_d = {
#     "referer": "",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
#     "cookie": "ubt_ssid=gj10m2ir1s2mspy7dg706vn0js6psq9o_2019-03-20; _utrace=d78c176a5d8890d24445cfa420b81fa5_2019-03-20; cna=6qeRFJNUxAMCAT2cydFg/fUc; eleme__ele_me=597ad32a9035a95ae5864d2162e13c9d%3A08c83c1c8529de4f8b019a90d0e74a2f44e740ba; track_id=1553086509|9166c6f7f0a679d36e2aad687322978e644b7aa604839d4666|f8e3fc3a47813d69da35afef54ab572b; USERID=2085922706; UTUSER=2085922706; SID=VyP55YxQjdiecmDu6gbYVfjjNlimz6DQc58w; isg=BKGhmss2WeUXJPUWSzXhQGY3sGt75hUozKog2AN3cKgHasw8V5zsEVeryd7J-a14; pizza73686f7070696e67=9n5StWrlVIv0LTcR6n8rV0HbmLsXstUddolO1nIh6pZwLZXRO1WkpVG3-F-64Sck",
# }


def response(flow):
    ctx.log.info('>>>>>>>>>>><<<<<<<<<<<<<<<<<')
    url = flow.request.url
    # 网易新闻
    if 'www.ele.me/restapi/shopping/restaurants' in url:
        ctx.log.info('>>>>>>>>>>><<<<<<<<<<<<<<<<<')
        ctx.log.info('>>>>>>>>>>><<<<<<<<<<<<<<<<<')
        content = flow.response.content
        deal_text(content)
