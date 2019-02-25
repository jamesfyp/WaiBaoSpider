# -*- coding: utf-8 -*-
import time
import os
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    '''
    测试类继承该类
    封装常用的方法
    '''

    def __init__(self, driver):
        self.driver = driver

    # 打开对应URL浏览器
    def open_browser(self, url):
        self.driver.get(url)
        time.sleep(2)

    def get_driver(self):
        return self.driver

    def close_browser(self):
        self.driver.close()

    # 显性等待，设置了默认超时时间和检查时间间隔
    def domi_wait(self, max_second=20, check_second=0.7):
        wait = WebDriverWait(self.driver, max_second, check_second)
        return wait

    # 退出浏览器结束测试
    def quit_browser(self):
        self.driver.quit()

    def refresh_driver(self):
        self.driver.refresh()

    # 关闭当前窗口
    def close(self):
        try:
            self.driver.close()
        except NameError as e:
            pass

    # 浏览器截图，可以在报错的时候使用
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshots/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        print(screen_name)
        try:
            self.driver.get_screenshot_as_file(screen_name)
        except NameError as e:
            self.get_windows_img()