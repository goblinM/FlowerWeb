# coding=utf-8
from django import template
import time
import json

# 创建模板库的实例
register = template.Library()

@register.filter(name="showplace")
def showplace(val):
    t = ""
    if val == "furong":
        t = "芙蓉区"
    elif val == "kaifu":
        t = "开福区"
    elif val == "tianxin":
        t = "天心区"
    elif val == "yuelu":
        t = "岳麓区"
    else:
        t = "雨花区"
    return t