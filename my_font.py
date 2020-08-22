# -*- coding: UTF-8 -*-
from fontTools.ttLib import TTFont     # 导包

font = TTFont('4326c3b22fbd4e7a9fd3e3ea57e8a2732288.woff')    # 打开文件
font.saveXML('4326.xml')     # 转换成 xml 文件并保存