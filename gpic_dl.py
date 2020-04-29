# -*- coding: utf-8 -*-
import random, time, os, shutil
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote as up
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

'''
@FileName	:   gpic_dl.py
@Created   :   2020/04/17
@Updated  :   2020/04/18
@Author		:   goonhope@gmail.com
@Function	:   专利清单及全文下载_广东省知识产权公共信息综合服务平台（需要登录）
@url            ：  http://s.gpic.gd.cn/route/hostingplatform/search/searchIndex
'''


class ChromeDriver(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def init_page(self,url=r"http://s.gpic.gd.cn/route/hostingplatform/search/searchIndex"):
        self.driver.get(url)
        self.driver.implicitly_wait(2)

    def show(self,css,timeout=25, gone=False):
        located = EC.visibility_of_element_located((By.CSS_SELECTOR , css))
        try:
            ui.WebDriverWait(self.driver, timeout).until(located) if not gone else \
            ui.WebDriverWait(self.driver, timeout).until_not(located)
            return True
        except TimeoutException:
            return False

    def input_key(self,ids,css="input.el-input__inner"):
        if isinstance(ids,str):
            input_el = self.driver.find_element_by_css_selector(css)
            input_el.clear()
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
        time.sleep(0.5)

    def click_by_css(self, css="li.el-menu-item.pull-right a"):
        search_el = self.driver.find_element_by_css_selector(css)
        search_el.click()
        time.sleep(3)

    def download(self, css="label[class^=el-radio-button]",list_pdf=True,xn="公司"):
        ''''下载'''
        search_el = self.driver.find_elements_by_css_selector(css)
        num = 0 if list_pdf else 3  # 0 清单 3打包pdf文件
        search_el[num].click()
        self.click_by_css("div.el-col.el-col-24 > button")
        # time.sleep(slp)
        dcss = "div.el-col.el-col-24 > div > a"
        self.click_by_css(dcss) if self.show(dcss) else None
        xname = self.driver.find_element_by_css_selector(dcss).get_attribute("href")
        xname = up(os.path.split(xname)[-1])  # url解码
        move_file(xname, xn)

    def grapHtml(self, css="span[class^='infoInlineSpan']"):
        content = [x.text.split(":")[-1].strip() for x in self.driver.find_elements_by_css_selector(css)]
        content = "\t".join(content)
        [print(i, sep="\t") if _%5 != 4 else print(i) for _,i in enumerate(content)]

    def go(self,ids,company):
        """执行程序"""
        self.init_page()
        self.click_by_css()
        self.input_key(ids,)
        self.click_by_css("div.el-form-item__content>button")
        self.input_key(company)
        self.click_by_css("button")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.click_by_css("div.tool-item>div>button")
        time.sleep(random.uniform(2,3))
        self.click_by_css("div>div.tool-item>a")
        self.download(xn=company)  # 下载list
        self.click_by_css("div.el-col.el-col-24 > button")  # 关闭
        self.click_by_css("div>div.tool-item>a")
        self.download(xn=company,list_pdf=False) # 下载pdf
        self.driver.quit()


def move_file(xname,xn,show=True):
    ''''移动到指定目录'''
    dir_default = r"D:\Downloads"  # chrome 默认下载目录
    subdir = r"D:\Temp" # 移动到目录
    xo = os.path.join(dir_default, xname)
    for x in ["有限公司","科技"]: xn = xn.replace(x,"")
    xn = xn + "_专利清单_2020" + os.path.splitext(xname)[-1]
    fxn = os.path.join(dir_default, xn)
    time.sleep(2) if not os.path.exists(xo) else None  # 等待文件下载
    os.renames(xo, fxn)
    time.sleep(2)
    oxn = os.path.join(subdir, xn)  # 最终文件
    os.remove(oxn) if os.path.exists(oxn) else None  # 二次删除原有
    shutil.move(fxn, subdir)  # 移动
    os.system("start %s" % subdir) if show else None
    return True if os.path.exists(oxn) else False


def main():
    """专利 下载"""
    company = input("查询：")
    ids = ("*************","*****")  # 账号密码
    driver = webdriver.Chrome()
    cd = ChromeDriver(driver)
    try:
        cd.go(ids, company)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
