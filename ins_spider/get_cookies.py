# -*- coding:utf-8 -*-
from selenium import webdriver
from base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

username = "hotjameschang"
passwd = "zjWWW1999"
login_url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
# 事件参数
user_box = (By.NAME, 'username')  # 账号
passwd_box = (By.NAME, 'password')  # 密码
login_btn = (By.XPATH, "//button[@type='submit']")  # 确认登陆
check_link = (By.XPATH, "//a/span[@aria-label='个人主页']")  # 检查是否登陆成功


class GetCookie(BasePage):
    '''
    获取cookies
    '''
    def login(self, wait):
        self.driver.find_element(*user_box).send_keys(username)
        self.driver.find_element(*passwd_box).send_keys(passwd)
        self.driver.find_element(*login_btn).click()
        wait.until(EC.presence_of_element_located(check_link))
        cookies = self.driver.get_cookies()
        return cookies


def getcookies():
    # 生成浏览器实例
    driver = webdriver.Chrome()
    # 生成GetCookies对象
    GC = GetCookie(driver)
    # 打开url
    GC.open_browser(login_url)
    # 生成显性等待实例
    wait = GC.domi_wait()
    # 登陆
    cookies = GC.login(wait)
    GC.close_browser()
    return cookies
