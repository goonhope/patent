# -*- coding: utf-8 -*-
import random, time, os, shutil
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote as up
'''
@FileName	:   sipo_info_gk.py
@Created     :   2018/04/26
@Updated    :   2020/04/26
@Author		:   goonhope@gmail.com
@Function	:   获取中国专利查询系统信息
'''


class FoxDriver(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def init_page(self,url):
        self.driver.get(url)
        self.driver.implicitly_wait(2)

    def input_key(self,ids,css="span.input_text > input",slp=3):
        if isinstance(ids,str):
            input_el = self.driver.find_element_by_css_selector(css)
            ActionChains(self.driver).double_click(input_el).perform()
            # input_el.clear()
            input_el.send_keys(ids)
        else:
            input_el = self.driver.find_elements_by_css_selector(css)[:2]
            if len(ids) == len(input_el):
                for x,i in zip(input_el,ids):
                    ActionChains(self.driver).double_click(x).perform()
                    # x.clear()
                    x.send_keys(i)
            else:
                print("check input_key function")
        time.sleep(slp)

    def click_by_css(self, css="input.login_butt",slp=3):
        search_el = self.driver.find_element_by_css_selector(css)
        search_el.click()
        time.sleep(slp)

    def get_content(self):
        total = ["data-totalpage", "data-totalrow"]
        list_count = [int(self.driver.find_element_by_css_selector("ul.pagination").get_attribute(val)) for val in total]
        print("{}总共申请专利{}条".format("公司", list_count[1]))
        for i in range(list_count[0]):  # 循环获取总数据
            if i:
                self.driver.find_element_by_css_selector(
                "body>div.bd>div.main_body>div.main_box>ul>li:nth-child(4)>a").click()
                time.sleep(2)
            list_hold = [x.text for x in self.driver.find_elements_by_css_selector("div.content_listx2")]
            print("\n".join(list_hold))

    def go(self,ids):
        """执行程序"""
        url = r"http://cpquery.sipo.gov.cn/"
        self.init_page(url)
        while 1:
            self.input_key(ids[:2])
            self.driver.execute_script("alert(\"请在8s内点击字体验证\");")
            time.sleep(1)
            self.driver.switch_to.alert.accept()
            self.click_by_css("#selectyzm_text_dz")
            time.sleep(8)  # 手动输入验证麻烦
            self.click_by_css()
            if self.driver.current_url != url : break
        self.click_by_css("#agreeid",slp=1)
        self.click_by_css("#goBtn")
        self.input_key(ids[2], r"#select-key\3a shenqingrxm")
        self.click_by_css("#query")
        self.get_content()
        # time.sleep(60*5)
        self.driver.quit()


def main():
    ids = ("91440*************", "*******","***限公司")  # 账号 密码 公司名称
    driver = webdriver.Firefox()
    cd = FoxDriver(driver)
    try:
        cd.go(ids)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
