# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time,random,os
from selenium import webdriver
from faker import Faker
#google专利抓取 by申请人 or 关键词 or 发明人


def get_patents_list(word, App_or_key=True):
    '''google 专利下载专利文件及 生成专利清单，默认申请人'''
    keys = f"assignee={word}" if App_or_key else f"q={word}"  # inventor=任
    main_url = r'https://patents.google.com/?{0}&language=CHINESE&num=50'.format(keys)
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')  # 后台运行
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    # driver.maximize_window()  # 最大化
    # driver.set_window_size(1200, 800) # 大小
    driver.implicitly_wait(1)
    driver.get(main_url)
    print(main_url)

    #pdf 下载接口
    pdfs = [i.get_attribute("href") for i in driver.find_elements_by_css_selector('a.pdfLink.style-scope.search-result-item')]
    names = [i.text + ".pdf" for i in driver.find_elements_by_css_selector('h3 span#htmlContent.style-scope.raw-html')]
    names = [x.replace("/","") for x in names]
    nums = [i.text for i in driver.find_elements_by_css_selector('span.style-scope.search-result-item') if "CN" in i.text]
    nums = [x for x in list(set(nums)) if len(x) != 2]
    file_name_url = zip(pdfs,names)
    # urls = [i.get_attribute("href") for i in driver.find_elements_by_css_selector('state-modifier>a')]
    dl_dir = r"D:\Temp\{}".format(word)
    os.makedirs(dl_dir) if not os.path.exists(dl_dir) else None
    download(main_url,file_name_url,dl_dir)

    utilitys, invents, publics = 0, 0, 0
    for num in nums:
        url = r"https://patents.google.com/patent/{0}/zh?assignee={1}&language=CHINESE&num=100".format(num,word)
        # detail page
        driver.get(url)
        time.sleep(random.uniform(1,2))
        inventor = "、".join([x.text for x in driver.find_elements_by_css_selector("dl[class^=important-people]>dd")][1:])
        info = [x.text for x in driver.find_elements_by_css_selector("div[class^=event]")]
        try:
            name = driver.find_element_by_css_selector("h1#title").text
            company = info[1].split("by")[-1].strip()
            nos = info[2].split("to")[-1].strip()
            grant = "granted" if "".join(info).find("granted") != -1 else "Publication"
            utilitys += 1 if nos[6] == "2" and grant == "granted" else 0
            invents += 1 if nos[6] == "1" and grant == "granted" else 0
            publics += 1 if grant == "Publication" else 0
            infos = [nos, name,company, inventor, grant, utilitys, invents, publics]
            infos = [str(x) for x in infos]
            print("\t".join(infos))
            # time.sleep(2400)
        except Exception as e:
            print("error check proxy ",e)
            pass
    driver.quit()
    os.system(r"start %s" % dl_dir)

    
def download(url, url_hrefs, path=""):
    ''''下载文件__url_hrefs为'''
    path = path if os.path.isdir(path) else r"D:\Temp"
    import urllib.request as req
    from urllib.parse import urljoin
    opener = req.build_opener()  # urlretrieve add header
    opener.addheaders = [('User-Agent', fr.chrome())]
    req.install_opener(opener)
    urls_root = url[:url.rindex("/") + 1]
    for url_href, filename in url_hrefs:
        pathfile = os.path.join(path, filename)
        url_all = urljoin(url, url_href)
        req.urlretrieve(url_all, pathfile)
    return True    

    
def main():
    start = time.time()
    word = input('请输入公司名：')
    get_patents_list(word, App_or_key=True)
    done = time.time()
    print("用时{0:.2f}s".format(done - start))


if __name__ ==  '__main__':
    main()
