# -*- coding:utf-8 -*-
# @Author: james
# @Date: 2019/3/20
# @File: main.py
# @Software: PyCharm
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

item = {
    "rating":"",
    "regular_customer_count":"",
    "has_story":"",
    "recommend_reasons":"",
    "flavors":"",
    "rating_count":"",
    "opening_hours":"",
    "recent_order_num":"",
    "float_minimum_order_amount":"",
    "theme":"",
    "float_delivery_fee":"",
    "is_valid":"",
    "max_applied_quantity_per_order":"",
    "latitude":"",
    "longitude":"",
    "status":"",
    "description":"",

    "piecewise_agent_fee":"",
    "phone":"",
    "address":"",
    "posters":"",
    "distance":"",
    "updatetime":"",
    "name":"",
    "type":"",
    "authentic_id":"",
    "next_business_time":"",
    "only_use_poi":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
    "description":"",
}

driver = webdriver.Chrome("./chromedriver")

list_url = "https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={gh}&latitude={la}&limit=24&longitude={lo}&offset={of}&terminal=web"

driver.get("https://h5.ele.me/login/#redirect=https%3A%2F%2Fwww.ele.me")
wait = WebDriverWait(driver, 100, 0.7)
wait.until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='map-header-right ng-scope']/a[@class='ng-binding']")))
print("yes")
driver.find_element_by_xpath("//input[@ng-model='search.keyword']").send_keys(u"烟台")
wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@ng-click='search.chooseAction(suggest)'])[1]")))
driver.find_element_by_xpath("(//li[@ng-click='search.chooseAction(suggest)'])[1]").click()

base_url = driver.current_url
print(base_url)
cookies = driver.get_cookies()
session = requests.session()
for i in cookies:
    session.cookies.set(i['name'], i['value'])
driver.close()
geohash = re.search("ele\.me/place/(.*)\?", base_url).group(1)
la = re.search("latitude=(\d+\.\d+)", base_url).group(1)
lo = re.search("longitude=(\d+\.\d+)", base_url).group(1)
of = 24
the_url = list_url.format(la=la, lo=lo, of=of, gh=geohash)
print(the_url)
res = session.get(the_url).text
respp = json.loads(res)
for info in respp:

