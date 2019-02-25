# -*- coding:utf-8 -*-
import json
import time
import datetime
import requests
from get_cookies import getcookies
from csvWriter import CSVDumper
from urllib import quote

dumper = CSVDumper("ins_test.csv")


def deal_ntr(text):
    content = text.strip().replace(u"\n", u"").replace(u"\t", u"").replace(u"\r", u"").replace(u" ", u"").replace(
        u"&nbsp", u"")
    return content


cookies = getcookies()
session = requests.session()
session.adapters.DEFAULT_RETRIES = 5
for i in cookies:
    session.cookies.set(i['name'], i['value'])
base_url = "https://www.instagram.com/graphql/query/?query_hash=f92f56d47dc7a55b606908374b43a314&variables=%7B%22tag_name%22%3A%22{key_word}%22%2C%22show_ranked%22%3Afalse%2C%22first%22%3A6%2C%22after%22%3A%22{after}%22%7D"
get_user_url = "https://www.instagram.com/graphql/query/?query_hash=292c781d60c07571d58d9ef7808888ef&variables=%7B%22shortcode%22%3A%22{uid}%22%2C%22include_reel%22%3Atrue%2C%22include_logged_out%22%3Afalse%7D"
start_after = "QVFDU2JuMHBQVG1IdlJnbGZTOGRrdTcyTy1fblA5blJWU2l4cl9yVUN5VnVMOWJ5bW00U190b3Q3V0JIZS1zTU5KSmdJUnFveUxqMGRYM2x1SF93RFNhSw=="
keyword = "面膜"
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}

FLAG = True

# while FLAG:
url = base_url.format(key_word=quote(keyword), after=quote(start_after))
print(url)
res = session.get(url, headers=headers).text
print(res)
if res:
    resp = json.loads(res)
    start_after = resp["data"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
    data = resp["data"]["hashtag"]["edge_hashtag_to_media"]["edges"]
    print(len(data))
    for info in data:
        item = {}
        p_time = info["node"]["taken_at_timestamp"]
        if p_time > 1546185600:  # 大于2018-12-31
            print("time to big")
            break
        elif p_time < 1530374400:
            print("time to small and finish")
            FLAG = False
            break
        else:
            print("start one page")
            pass
        item[u"帖子id"] = "'{}'".format(info["node"]["id"])
        print(item[u"帖子id"])
        item[u"作者id"] = info["node"]["owner"]["id"]
        item[u"短id"] = info["node"]["shortcode"]
        item[u"发帖时间本地"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p_time))
        item[u"发帖时间utc"] = datetime.datetime.utcfromtimestamp(p_time).strftime("%Y-%m-%d %H:%M:%S")
        content_list = info["node"]["edge_media_to_caption"]["edges"]
        base_str_list = []
        for i in content_list:
            base_str_list.append(i["node"]["text"])
        content = deal_ntr("".join(base_str_list))
        item[u"发帖正文"] = content
        item[u"帖子链接"] = "https://www.instagram.com/p/{}/".format(item[u"短id"])
        item[u"评论数"] = info["node"]["edge_media_to_comment"]["count"]
        item[u"点赞数"] = info["node"]["edge_media_preview_like"]["count"]
        item[u"图片链接1"] = info["node"]["display_url"]
        item[u"图片链接2"] = info["node"]["thumbnail_resources"][-1]["src"]
        # user_res = session.get(get_user_url.format(uid=item[u"短id"])).json()
        # print(user_res)
        # item[u"发帖作者"] = user_res["data"]["shortcode_media"]["owner"]["reel"]["owner"]["username"]
        dumper.process_item(item)
    # print(res)
