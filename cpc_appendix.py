# -*- coding: utf-8 -*-
'''
@FileName	:   cpc_appendix.py
@Created  :   2019/04/30
@Updated  :   2019/04/30
@Author		:   goonhope@gmail.com,
@Function	:   CPC 附件图片处理——调用cmd处理
@Environment：Imagemagick、ghostscript
'''

import os,time
from PIL import Image


def pdf_2_img(path, dpi=300,show=False):
    '''pdf转为图片'''
    cmd = f"for %i in ({path}\*.pdf)  do magick convert -density \
                {dpi} -quality 100 %i %~dpni_%03d.jpg"
    keys = f'chcp 65001 && {cmd}' # cmd字符代码UTF8 ，window 默认936-GBK
    rezt = os.popen(keys).read()
    print(rezt) if show else None


def img_resize(path, scale=0.25, subdir=True,show=False):
    '''pdf转为图片'''
    outpath = os.path.join(path, r"done") if subdir else path
    os.makedirs(outpath) if not os.path.exists(outpath) else None
    mid = "done\\" if subdir else ""
    cmd = f"for %i in ({path}\*.jpg)  do magick convert -resize \
                {scale*100}% %i %~dpi{mid}%~nxi"
    keys = f'chcp 65001 && {cmd}'  # cmd字符代码UTF8 ，window 默认936-GBK
    rezt = os.popen(keys).read()
    print(rezt) if show else None


def get_img_names(path, inname=".",ext="img"):
    '''获取含有特定字符的图片文件名，默认全部'''
    img_extend = ['jpg', 'jpeg', 'tiff', 'tif', 'png', "bmp"]
    img_extend = img_extend if ext == "img" else [ext]
    file_hold = [x for x in os.listdir(path) if (x.split(".")[-1].lower() in img_extend and inname in x)]
    return file_hold


def img_scale(path_in):
    '''获取图片resize比例'''
    file = get_img_names(path_in)[0]
    img = Image.open(os.path.join(path_in, file))
    width, height = img.size
    scale = round(width/620,2)
    return 1/scale if scale > 1 else "check"


def main():
    ''''默认PDF300dpi转图片resize25%合格，其它情况调用iimg_scale获取比例'''
    path = input("输入PDF文件路径：")
    pdf_2_img(path)
    time.sleep(5)
    img_resize(path)


if __name__ == "__main__":
    main()
