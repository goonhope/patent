# -*- coding: utf-8 -*-
import os, shutil, cchardet, time, img2pdf, zipfile,xlwt
from lxml import etree as et

'''
@FileName	:   cpc_img2pdf.py
@Created    :   Oct,2018
@Update     :   May,2020
@Author		:   goonhope@gmail.com
@Function	:   专利申请中间文件批量归档，xml to list
'''

def file_encoding(file_in):
    '''文件编码查询'''
    with open(file_in, 'rb') as f:
        data = f.read()
    return cchardet.detect(data)['encoding']


def read_xml(xml_f, encod="GBK"):
    '''读取xml文件待改进'''
    parser = et.XMLParser(encoding=encod, load_dtd=True)  # list GBK other
    root = et.parse(xml_f, parser).getroot()
    tex = root.xpath("//FAMINGMC")[0].text
    all_text = {x.tag:x.text for x in root.xpath("//*")}
    # all_text = [x.strip() for x in root.itertext() if x.strip()]
    all_dict = {x.tag : x.text.strip() for x in root.cssselect("*") if x.text is not None}
    all_dict = {x:y for x,y in all_dict.items() if y.strip()}
    all_dict["WENJIANMC"] = [x.text for x in root.cssselect("WENJIANMC")]
    # all_text ={x:y.strip() for x,y in all_text.items() if len(y) >= 3}
    return all_dict


def tiftopdf(location):
    '''批量转成pdf文件'''
    newhold = ["_".join(x.split("_")[:-1]) for x in os.listdir(location) if x.endswith(".tif")]
    newhold_unqe = list(set(newhold))
    num = len(newhold_unqe)
    for x in newhold_unqe:
        new = [y for y in os.listdir(location) if "_".join(y.split("_")[:-1]) == x ]
        img_to_pdf(location, new)
    print("已生成{}个pdf文件".format(num)) if num else None


def img_to_pdf(path, images):
    # 图片转pdf 默认布局
    # a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    # layout_fun = img2pdf.get_layout_fun(a4inpt)
    images = [os.path.join(path,x) for x in images]
    with open(os.path.splitext(images[0])[0][:-3] + '.pdf', "wb") as f:
        # f.write(img2pdf.convert(images,layout_fun=layout_fun))
        f.write(img2pdf.convert(images))


def timer(func):
    '''默认计时装饰器'''
    def wrapper(*args, **kwargs):
        start = time.time()
        print("处理中...")
        location, n = func(*args, **kwargs)
        print(f"@{func.__name__}:\t[Time:{time.time() - start : 0.3f}s]\t[归档数量:{n}条]，清单如下：")
        print("\n".join(os.listdir(location)))
        return
    return wrapper


def copy_req_dirs(source,location,mtime):
    """复制符合要求的文件夹，后期可能需要修改"""
    dirs = os.listdir(source)
    for sor in dirs:
        fsor = os.path.join(source,sor)
        if os.path.isdir(fsor):
            lsor = os.path.join(location,sor)
            if sor.startswith("GA") or sor.startswith("14"):
                if os.path.getmtime(fsor) >= time.mktime(time.strptime(mtime, "%Y%m%d")):
                    shutil.copytree(fsor, lsor)
    time.sleep(1)


def xf(path,delta=True):
    '''压缩文件解压后删除'''
    rarlist = ["zip","rar"]
    rar_dir = [x for x in os.listdir(path) if x.split(".")[-1].lower() in rarlist] if \
        os.path.isdir(path) else [os.path.split(path)[-1]]
    path = path if os.path.isdir(path) else os.path.split(path)[0]
    if rar_dir:
        for rar in rar_dir:
            f = zipfile.ZipFile(os.path.join(path, rar), 'r')
            # sub_dir = os.path.join(path, f'{rar.split(".")[0]}')
            sub_dir = os.path.join(path, f"{rar[:rar.rfind('.')]}")
            for file in f.namelist():
                f.extract(file, sub_dir)  # 将压缩包里的word文件夹解压出来
            f.close()
            for root, dirs, files in os.walk(sub_dir, topdown=False):
                for name in files:
                    gname = name.encode('cp437').decode("GBK")
                    if name != gname:
                        old = os.path.join(root, name)
                        newname = os.path.join(root, name.encode('cp437').decode("GBK"))
                        os.renames(old, newname)   # 修正编码
                for dir in dirs:
                    gdir = dir.encode('cp437').decode("GBK")
                    if dir != gdir:
                        olddir = os.path.join(root, dir)
                        newnamedir = os.path.join(root, dir.encode('cp437').decode("GBK"))
                        os.renames(olddir, newnamedir)   # 修正编码
            os.remove(os.path.join(path, rar)) if delta else None  # 删除rar


@timer
def filed(location, source=False,mtime="20100102"):
    '''授权申请过程文件及证书批量重命名，默认直接复制CPC notices 目录'''
    if source:
        source = r"C:\Program Files (x86)\gwssi\CPC客户端\cases\notices"
        shutil.rmtree(location) if os.path.exists(location) else None  # 避免重复
        os.makedirs(location) if not os.path.exists(location) else None  # 建文件
        if os.path.exists(source):
            copy_req_dirs(source, location,mtime)  # 复制
        else:
            print("未安装cpc，请直接导出解压到location目录")
            return False
    dirs = [x for x in os.listdir(location) if os.path.isdir(os.path.join(location,x))]
    num = 0  # 计数
    intxt = ["受理","合格","实质","专利证书","审查意见","办理登记"]
    infos = [["发文序号","申请号","发明名称","通知书名称"],]
    for dir in dirs:
        xml_file = os.path.join(location, f"{dir}\\list.xml")
        if os.path.exists(xml_file):
            info = read_xml(xml_file)
            notice_name = info['TONGZHISMC']  # 通知书名称
            if any(x in notice_name for x in intxt):
                notice_id = info['TONGZHISID']  # 通知书id
                appdx = info["WENJIANMC"]  # 附件
                app_id = info['SHENQINGH']  # 申请号
                invt_name = info['FAMINGMC']  # 发明名称
                infos.append(["'" + notice_id,"'" + app_id,invt_name,notice_name])
                sub_dir = os.path.join(location, f"{dir}\\" + f"{notice_id}\\" * 2) # 直接根目录
                sub_files = get_files(sub_dir)
                for sub_f in sub_files:
                    old_file = os.path.join(sub_dir, sub_f)
                    appendix = ".pdf" if "证书" in notice_name else f"_{sub_f[-6:]}"
                    new_sub_f = f"{app_id}_{invt_name}_{notice_name}" + appendix
                    new_sub_f = new_sub_f.replace("第N次", "第1次") if "第N次" in new_sub_f else new_sub_f
                    fnum = len(get_files(location,iname=new_sub_f,ext="tif"))  # 计算已有数量
                    new_sub_f = new_sub_f.replace("第1次",f"第{fnum + 1}次") if num and "第1次" in new_sub_f else new_sub_f
                    new_file = os.path.join(location, new_sub_f)
                    os.renames(old_file,new_file)
                    time.sleep(1)
                    num += 1
                condtion = any(x in notice_name for x in intxt[-2:]) if appdx else False
                if condtion:  # 附件
                    sub_dir = os.path.join(location, f"{dir}\\{notice_id}")
                    for nu,wjc in enumerate(appdx):
                        wjc_zip = os.path.join(sub_dir, wjc)
                        wjc_dir = os.path.splitext(wjc_zip)[0]
                        xf(wjc_zip) if not os.path.exists(wjc_dir) else None  # 解压zip
                        time.sleep(1)
                        sub_files = get_files(wjc_dir)
                        for sub_f in sub_files:
                            old_file = os.path.join(wjc_dir, sub_f)
                            mid = f"_授权通知书_{nu}" if intxt[-1] in notice_name else f"检索or对比_{nu}"
                            new_sub_f = f"{app_id}_{invt_name}_{mid}_" + sub_f[-6:]
                            new_file = os.path.join(location, new_sub_f)
                            # 删除 授权通知书的检索文件
                            os.renames(old_file, new_file) if not (nu > 0 and "授权通知书" in new_sub_f) else None
                            time.sleep(1)
                            num += 1
    [shutil.rmtree(os.path.join(location, x)) for x in dirs]  # 删除目录txt
    save_to_excel(infos, os.path.join(location,"list.xls"))
    tiftopdf(location)  # 转成pdf文件
    os.system("start %s" % location)
    return location, num


def get_files(path,ext=("tif","tiff","pdf"),iname=""):
    """获取pdf 、tif文件"""
    files = [x for x in os.listdir(path) if x.split(".")[-1].lower() in ext \
               and  iname in x]
    return files


def save_to_excel(info,file_out):
    '''写入excel,info二维数组 [[]]'''
    file = xlwt.Workbook()
    table = file.add_sheet('list', cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    for i in range(len(info)):  # 行 y-->Row
        for j in range(len(info[i])):  # 列 x--> Column
            table.write(i, j, info[i][j], style)
    file.save(file_out)


def main():
    path = input("输入归档或压缩包目录： ").strip()
    if path.endswith(".zip") and os.path.exists(path):
        xf(path)  # zip 解压
        path = os.path.splitext(path)[0]
        filed(path)
    elif not os.path.exists(path):  # 新目录默认直接copy notices文件 到path文件
        filed(path,True,mtime="20200515")
    else:
        filed(path)  # 已解压目录


if __name__ == '__main__':
    main()
