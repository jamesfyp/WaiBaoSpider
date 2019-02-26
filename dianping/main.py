# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/2/25
# @File: main.py
# @Software: PyCharm

import random
import time

import re
import traceback

from dateformatting import dateformatting
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from csvWriter import CSVDumper
from svg_t import get_big_box
from svg import get_big_box2

name = time.strftime('%Y-%m-%d+%H+%M+%S', time.localtime(time.time()))
dumper = CSVDumper(name + '_Comment.csv')


def domi_wait(driver, max_second=20, check_second=0.7):
    wait = WebDriverWait(driver, max_second, check_second)
    return wait


# 登陆-------------
check_link = (By.XPATH, "//span[@class='userinfo-container']")  # 检查是否登陆成功
chrome_options = Options()
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.{}.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'.format(
        str(random.randrange(1100, 9250))))
driver = webdriver.Chrome(chrome_options=chrome_options)
wait = domi_wait(driver, max_second=60)
driver.get("https://www.dianping.com/login?redir=https://www.dianping.com/")
wait.until(EC.presence_of_element_located(check_link))
print("Login Success!!!")
base_url = "http://www.dianping.com/shop/{}/review_all?queryType=sortType&queryVal=latest"

# 加载商店列表
keys = []
with open('shop.txt') as f:
    for line in f.readlines():
        keys.append(line.strip().replace("\xc2\xa0", ''))


def pf_biaoz(pl):
    if u'差' in pl:
        return '0'
    elif u'不佳' in pl:
        return '0'
    elif u'一般' in pl:
        return '1'
    elif u'满意' in pl:
        return '2'
    elif u'很好' in pl:
        return '3'
    elif u'不错' in pl:
        return '3'
    elif u'超棒' in pl:
        return '4'
    elif u'非常好' in pl:
        return '4'
    elif u'好' in pl:
        return '2'
    else:
        return pl


def get_one_page(driver, url, word_box=None):
    print(url)
    while True:
        driver.get(url)
        if "verify.meituan.com" in driver.current_url:
            print u'请复制滑动解锁的URL到其他浏览器解锁后按回车重试!'
            raw_input()
        else:
            break
    fold_list = driver.find_elements_by_xpath("//div[@class='more-words']/a[@class='fold']")
    if len(fold_list) > 0:
        for fold in fold_list:
            fold.click()
    html = etree.HTML(driver.page_source)
    # 添加 评论总量
    all_comment = html.xpath('//em[@class="col-exp"]//text()')[0].replace('(', '').replace(')', '') if html.xpath(
        '//em[@class="col-exp"]//text()') else 0
    dianpu_name = html.xpath("//h1[@class='shop-name']/text()")[0].strip() if html.xpath(
        "//h1[@class='shop-name']/text()") else ""
    # # 处理缺字问题
    if not word_box:
        css_urls = html.xpath('//link[@rel="stylesheet"]/@href')
        for css_url in css_urls:
            if 's3plus.meituan.net' in css_url:
                css_url = 'https:' + css_url
                try:
                    word_box = get_big_box(css_url)
                    print word_box
                    print u'缺字分析初始化成功！'
                except:
                    print traceback.format_exc()
                    try:
                        word_box = get_big_box2(css_url)
                    except:
                        print traceback.format_exc()
                        print u'缺字分析失败！请截图给技术'
    eles = html.xpath("//div[@class='reviews-items']/ul/li")
    print(len(eles))
    for line in eles:
        print u'>>>回复<<<<'
        result = {}
        result[u'url'] = url
        author = line.xpath(".//a[@class='name']/text()")
        if not author:
            author = line.xpath(".//span[@class='name']/text()")
        result[u'作者'] = author[0].strip().replace(' ', '')
        comm = line.xpath(".//div[@class='review-words']")
        # 评论处理
        com_fin = []
        single = word_box["single"]
        for com in comm:
            try:
                mstr = etree.tostring(com, encoding="utf-8", pretty_print=True).strip().decode('utf-8')
                rest = re.sub(
                    r'class=".*?"|<div.*?div>|</span>|<span class="|"/>|">|<br/>',
                    '', mstr)
                word = re.findall('(' + single + '[0-9A-Za-z]{3})', rest)
                for w in word:
                    try:
                        rest = rest.replace(w, word_box[w])
                    except:
                        print 'NOT', w
                htmls = etree.HTML(rest)
                com_fin = htmls.xpath('//div/text()')
            except:
                print traceback.format_exc()
                print u'处理评论失败,请截图给技术'
        comms = ''.join(com_fin)
        result[u'评论内容'] = comms.strip().replace(u'\xa0', ' ') if comm else ''
        datetime = line.xpath(".//span[@class='time']/text()")[0].strip()
        datetime = re.search('(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', datetime).group(1)
        result[u'日期'] = dateformatting.parse(datetime).strftime('%Y-%m-%d %H:%M:%S')
        xg = line.xpath(".//span[@class='score']/span[1]/text()")
        sz = line.xpath(".//span[@class='score']/span[2]/text()")
        hj = line.xpath(".//span[@class='score']/span[3]/text()")
        xgg = xg[0].strip().replace(' ', '').replace(
            u'效果：', '') if xg else '0'
        szz = sz[0].strip().replace(' ', '').replace(
            u'师资：', '') if sz else '0'
        hjj = hj[0].strip().replace(' ', '').replace(
            u'环境：', '') if hj else '0'
        result[u'效果'] = pf_biaoz(xgg)
        result[u'师资'] = pf_biaoz(szz)
        result[u'环境'] = pf_biaoz(hjj)

        result[u'店铺总评论量'] = all_comment
        result[u'店铺名称'] = dianpu_name

        starts = line.xpath(".//div[@class='review-rank']/span[1]/@class")[0]
        starts = re.search('(\\d+)', starts).group(1)
        result[u'评分'] = int(starts) / 10
        like = line.xpath('.//em[@class="col-exp"]/text()')
        result[u'赞'] = like[0].replace('(', '').replace(')', '') if like else '0'
        # rep = line.xpath(".//p[@class='shop-reply-content Hide']/text()")
        # # 经过矫正的回复
        # result[u'回应'] = rep[0].strip().replace(u'\xa0', ' ') if rep else ''
        # result[u'回应时间'] = '-'
        # if result[u'回应']:
        #     rept = line.xpath('.//div[@class="shop-reply"]//span[@class="date"]/text()')
        #     result[u'回应时间'] = rept[0]
        dumper.process_item(result)

        # more = line.xpath(".//div[@class='more-related-reviews']")
        # if more:
        #     uid = line.xpath(".//div[@class='more-related-reviews']/a/@data-userid")[0]
        #     print uid
        #     req = requests.get(more_comment.format(uid=uid, shop=shop), headers=header)
        #     js = json.loads(req.text)
        #     a = js.get('msg')
        #     if not a:
        #         # 如果没有得到折叠数据
        #         print u'折叠数据加载失败-请查看结果数据并手动补充'
        #         result[u'评论内容'] = u'【这是一条折叠评论,但是抓取异常失败,请访问网页版查看该条】'
        #         dumper2.process_item(result)
        #         continue
        #     html_m = etree.HTML(a)
        # print js.get('msg')
        # 处理是否有被折叠的更多评价
        #     line_mores = html_m.xpath('//div[@class="content"]')
        #     if line_mores:
        #         print 'YES MORE'
        #         for line_more in line_mores:
        #             datetime = line_more.xpath(".//span[@class='time']/text()")[0].strip()
        #             datetime = re.search('(\d{4}-\d{2}-\d{2})', datetime).group(1)
        #             result[u'日期'] = dateformatting.parse(datetime).strftime('%Y-%m-%d %H:%M:%S')
        #             comm = line_more.xpath(".//p[@class='desc']//text()")
        #             comm = ''.join(comm)
        #             result[u'评论内容'] = comm.strip().replace(u'\xa0', ' ') if comm else ''
        #
        #             xg = line_more.xpath(".//p[@class='shop-info']/span[2]/text()")
        #             sz = line_more.xpath(".//p[@class='shop-info']/span[3]/text()")
        #             hj = line_more.xpath(".//p[@class='shop-info']/span[4]/text()")
        #
        #             xgg = xg[0].strip().replace(' ', '').replace(
        #                 u'效果：', '') if xg else '0'
        #             szz = sz[0].strip().replace(' ', '').replace(
        #                 u'师资：', '') if sz else '0'
        #             hjj = hj[0].strip().replace(' ', '').replace(
        #                 u'环境：', '') if hj else '0'
        #             result[u'效果'] = pf_biaoz(xgg)
        #             result[u'师资'] = pf_biaoz(szz)
        #             result[u'环境'] = pf_biaoz(hjj)
        #             result[u'店铺总评论量'] = all_comment
        #             starts = line_more.xpath(".//p[@class='shop-info']/span[1]/@class")[0]
        #             starts = re.search('(\\d+)', starts).group(1)
        #             result[u'评分'] = int(starts) / 10
        #             like = line_more.xpath('.//a[@class="item J-praise"]/text()[2]')
        #             like = re.search('(\\d+)', like[0])
        #             result[u'赞'] = like.group(1) if like else '0'
        #         rep = line_more.xpath('.//a[@class="item"]/text()')[0]
        #         rep = re.search('(\\d+)', rep)
        #         # 经过矫正的回复
        #         result[u'回应'] = rep.group(1) if rep else ''
        #         result[u'回应时间'] = '-'
        #         if result[u'回应']:
        #             rept = line.xpath('.//div[@class="shop-reply"]//span[@class="date"]/text()')
        #             result[u'回应时间'] = rept[0]
        #         # print result
        #         dumper2.process_item(result)

    print u'当前页面抓取完成'
    time.sleep(15)
    return word_box
    # except:
    #     print traceback.format_exc()
    #     print u'当前店铺评论抓取失败!!', key
    #     time.sleep(10)


for shop_id in keys:
    print("start this shop %s" % shop_id)
    url = base_url.format(shop_id)
    word_box = get_one_page(driver, url)
    while driver.find_elements_by_class_name("NextPage"):
        next_url = driver.find_element_by_class_name("NextPage").get_attribute("href")
        get_one_page(driver, next_url, word_box)
    else:
        print("no last page and start next shop!!!!")
        continue
