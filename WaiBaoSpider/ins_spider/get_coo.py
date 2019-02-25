# -*- coding:utf-8 -*-
from selenium import webdriver
from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

username = "15506477707"
passwd = "zjWWW1999"
login_url = "https://account.dianping.com/login?redir=http%3A%2F%2Fwww.dianping.com%2F"
# 事件参数
button1 = (By.CLASS_NAME, "bottom-password-login")
button2 = (By.CLASS_NAME, "tab tab-account ")
user_box = (By.ID, 'account-textbox')  # 账号
passwd_box = (By.ID, 'password-textbox')  # 密码
login_btn = (By.ID, "login-button-account")  # 确认登陆
check_link = (By.XPATH, "//span[@class='userinfo-container']")  # 检查是否登陆成功


class GetCookie(BasePage):
    '''
    获取cookies
    '''
    def login(self, wait):
        wait.until(EC.presence_of_element_located(check_link))
        cookies = self.driver.get_cookies()
        return cookies


def getcookies():
    # 生成浏览器实例
    driver = webdriver.Chrome("/Users/james/PycharmProjects/WaiBaoSpider/WaiBaoSpider/ins_spider/chromedriver")
    # 生成GetCookies对象
    GC = GetCookie(driver)
    # 打开url
    GC.open_browser(login_url)
    # 生成显性等待实例
    wait = GC.domi_wait(max_second=60)
    # 登陆
    cookies = GC.login(wait)
    GC.close_browser()
    return cookies