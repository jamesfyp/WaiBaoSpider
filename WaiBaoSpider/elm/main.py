# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/20
# @File: main.py
# @Software: PyCharm
import time
import redis
import random

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

rediser = redis.Redis(host='127.0.0.1', port='6379', db=2, )

option = webdriver.ChromeOptions()
option.add_argument('--proxy-server=http://127.0.0.1:8000')
option.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
driver = webdriver.Chrome(executable_path="./chromedriver", options=option)

wait = WebDriverWait(driver, 30, 1)

driver.get("https://www.ele.me/")
# browser.add_cookie({"name": "cy", "value": "148"})
driver.add_cookie({"name": "ubt_ssid", "value": "gj10m2ir1s2mspy7dg706vn0js6psq9o_2019-03-20"})
driver.add_cookie({"name": "_utrace", "value": "d78c176a5d8890d24445cfa420b81fa5_2019-03-20"})
# driver.add_cookie({"name": "perf_ssid", "value": "1fqmr4i5i1mxun75cznm5ilz1p1u7atd_2019-03-20"})
driver.add_cookie({"name": "cna", "value": "6qeRFJNUxAMCAT2cydFg/fUc"})
driver.add_cookie(
    {"name": "eleme__ele_me", "value": "597ad32a9035a95ae5864d2162e13c9d%3A08c83c1c8529de4f8b019a90d0e74a2f44e740ba"})
driver.add_cookie({"name": "track_id",
                   "value": "1553086509|9166c6f7f0a679d36e2aad687322978e644b7aa604839d4666|f8e3fc3a47813d69da35afef54ab572b"})
driver.add_cookie({"name": "USERID", "value": "2085922706"})
driver.add_cookie({"name": "UTUSER", "value": "2085922706"})
driver.add_cookie({"name": "SID", "value": "epYbo22nwVC6mtqZLZ5ZbtChe1XtKICNYcvA"})
driver.add_cookie({"name": "isg", "value": "BFlZcOTUYVBJPj3O062pqH4faEPzTk3hxLLooHsOiAD_gn0U2jSCaVGTgAZROuXQ"})
driver.add_cookie(
    {"name": "pizza73686f7070696e67", "value": "CPuz42fVoxnRVcVQ1x33fTPbVZfw-_INk1g5lYTK95HfJSSrfGpBaY62BOIYZvO1"})

for tag_num in range(700):
    ss = rediser.spop("beijingaddr")
    rediser.sadd("beijingaddr_back", ss)
    if ss:
        ss_list = ss.split("#$#$")
        count = int(ss_list[0])
        print("count: %s " % count)
        geo = ss_list[1]
        lo = ss_list[2]
        la = ss_list[3]
        print("start one localtion %s, %s" % (tag_num, geo))
        url = "https://www.ele.me/place/{geo}?latitude={la}&longitude={lo}".format(geo=geo, la=la, lo=lo)
        driver.get(url)
        ps = driver.page_source
        html = etree.HTML(ps)
        if html.xpath("//div[@class='login-for-more']"):
        # if driver.find_element_by_xpath("//div[@class='login-for-more']"):
            print("登陆过期！！！！！！！！！！！！！！！！！！！！！！！")
            break
        time.sleep(2)
        flag = True
        while flag:
            while True:
                a = driver.page_source
                print("start fan page")
                for i in range(20):
                    time.sleep(0.5)
                    driver.find_element_by_xpath("//html").send_keys(Keys.SPACE)
                    # focu = driver.find_element_by_xpath("//h5[@class='owner']")
                    # driver.execute_script("arguments[0].focus();", focu)
                b = driver.page_source
                if a == b:
                    break
                else:
                    continue
            while True:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='fetchMoreRst']")))
                except:
                    flag = False
                    break
                driver.find_element_by_xpath("//div[@id='fetchMoreRst']").click()
                time.sleep(random.randint(5, 15))
                break
    time.sleep(30)
