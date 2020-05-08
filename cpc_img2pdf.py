# -*- coding: utf-8 -*-
import os, re, shutil, cchardet, time
from lxml import etree as et
import img2pdf,zipfile

'''
@FileName	:   cpc_img2pdf.py
@Created  :   Oct,2018
@Author		:   goonhope@gmail.com
@Function	:   专利通知书批量重命名，转pdf文件—
                        CPC直接导出通知文件解压，读取list.xml 
                        信息在批量重命名，删除其它文件
'''


def file_encoding(file_in):
    '''文件编码查询'''
    with open(file_in, 'rb') as f:
        data = f.read()
    return cchardet.detect(data)['encoding']


def read_xml(xml_f,encod="UTF-8"):
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
                    old = os.path.join(root, name)
                    newname = os.path.join(root, name.encode('cp437').decode("GBK"))
                    os.renames(old, newname)   # 修正编码
                for dir in dirs:
                    olddir = os.path.join(root, dir)
                    newnamedir = os.path.join(root, dir.encode('cp437').decode("GBK"))
                    os.renames(olddir, newnamedir)   # 修正编码
            os.remove(os.path.join(path, rar))  if delta else None  # 删除rar


def rename(location):
    '''专利通知书图片重命名，并移动到根目录——单压缩包.'''
    dirs = [x for x in os.listdir(location) if "GA" in x]
    n = 1
    #  获取专利l信息list
    for dir in dirs:
        xml_name = os.path.join(location, f"{dir}\\list.xml")
        enc = file_encoding(xml_name)  # 获取文件编码
        with open(xml_name,"r", encoding=enc) as fi:
            f = fi.read()
            info = re.findall(r"<TONGZHISID>(.+)<", f) + re.findall(r"<SHENQINGH>(.+)<", f) \
                   + re.findall(r"<FAMINGMC>(.+)<", f) + re.findall(r"<TONGZHISMC>(.+)<", f) \
                   + re.findall(r"<WENJIANMC>(.+)<", f)
                   # + re.findall(r"<FAWENXLH>(.+)<", f)
                   #通知书ID、申请号、发明名称、通知书名称、授权通知书压缩包、发文序列号
            xf(os.path.join(location, f'{info[0]}\\' * 2)) if info[-1].endswith("zip") else None
        print(*info)
        # 重命名后移动到根目录——路径规律
        info_short = [x.strip(".zip") for x in info if "GA" in x or x.endswith("zip")]
        names_hold = ["", "授权通知书", "检索报告"]
        for info_in, name_mid  in zip(info_short,names_hold):
            imgdir = os.path.join(location, f'{info[0]}\\' * 2 + info_in)
            imgfiles = [x for x in os.listdir(imgdir)]
            for name in imgfiles:
                old = os.path.join(imgdir, name)
                num = 3 if name_mid else 4
                mid = f"_{name_mid}_" if name_mid else "_"
                newname = os.path.join(imgdir, "_".join(info[:num]) + mid + name[4:])
                os.renames(old, newname)
                n += 1
                shutil.move(newname, location)
    return location,n


def tiftopdf(location):
    '''批量转成pdf文件'''
    newhold = ["_".join(x.split("_")[:-1]) for x in os.listdir(location) if x.endswith(".tif")]
    newhold_unqe = list(set(newhold))
    for x in newhold_unqe:
        new = [y for y in os.listdir(location) if "_".join(y.split("_")[:-1]) == x ]
        img_to_pdf(location, new)
    print("已生成{}个pdf文件".format(len(newhold_unqe)))


def img_to_pdf(path, images):
    # 图片转pdf 默认布局
    # a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    # layout_fun = img2pdf.get_layout_fun(a4inpt)
    images = [os.path.join(path,x) for x in images]
    with open(os.path.splitext(images[0])[0][:-3] + '.pdf', "wb") as f:
        # f.write(img2pdf.convert(images,layout_fun=layout_fun))
        f.write(img2pdf.convert(images))


def delete(location):
    '''删除指定格式以外的文件和文件夹，显示文件名'''
    [shutil.rmtree(os.path.join(location, x)) for x in os.listdir(location) \
    if os.path.isdir(os.path.join(location, x)) ]
    os.system(r"start " + location)
    return None


def timer():
    '''默认计时装饰器'''
    def wrapper(*args, **kwargs):
        start = time.time()
        location, n = func(*args, **kwargs)
        print(f"@{func.__name__}:\t[Time:{time.time() - start : 0.3f}s]\t[归档数量:{n}]")
        print("\n".join(os.listdir(location)))
        return
    return wrapper



@timer
def appy(zipfile):
    xf(zipfile)
    time.sleep(1)
    location = os.path.splitext(zipfile)[0]
    n = rename(location)
    delete(location)  # 删除非tif文件
    tiftopdf(location)  # 转成pdf文件
    # delete(location,"pdf")  # 删除非pdf文件
    os.system("start %s" % location)
    return location,n


@timer
def grant(zipfile):
    '''授权专利证书批量重命名'''
    location = os.path.splitext(zipfile)[0]
    xf(zipfile)
    time.sleep(1)
    dirs = [x for x in os.listdir(location) if x.startswith("144O")]
    num = 0
    for dir in dirs:
        xml_file = os.path.join(location, f"{dir}\\list.xml")
        if os.path.exists(xml_file):
            info = read_xml(xml_file, "GBK")
            if "专利证书" in info['TONGZHISMC']:
                shortn_name = f"{info['SHENQINGH']}_{info['FAMINGMC']}_证书.pdf"
                old_name = os.path.join(location,f"{dir}\\" + f"{dir[:-2]}\\" *2 + f"{dir[:-2]}.pdf")
                shutil.move(old_name,location)
                fn_name = os.path.join(location, f"{dir[:-2]}.pdf")
                time.sleep(0.5) if os.path.exists(fn_name) else None
                nw_name = os.path.join(location,shortn_name)
                os.rename(fn_name,nw_name)
                num += 1
    [shutil.rmtree(os.path.join(location,x)) for x in dirs]
    os.system("start %s" % location)
    return location,num


if __name__ == '__main__':
    zipfile = input("输入导出zip文件路径：").strip()
    # appy(zipfile)  # 申请文件归档
    grant(zipfile) # 证书文件归档
