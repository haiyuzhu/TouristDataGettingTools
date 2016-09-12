# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:54:57 2016

@author: haiyuzhu
"""

import requests
import json
import os
import datetime
import time
import random
from bs4 import BeautifulSoup

host = "http://218.94.79.6:8095"
cookie = "JSESSIONID=3BDAB7CA93A31FEFFD4C53C04757E24A"


def get_cookie():
    resp = requests.get(url=host + "/kyfx/info/login.jsp")
    cookie = resp.headers['set-cookie']
    resp = requests.get(url=host + "/kyfx/info/yanzhengma.jsp", headers={"cookie": cookie})

    file = open(os.getcwd() + "/ver.jpg", "wb+")
    file.write(resp.content)
    file.close()
    ver_code = input()
    resp = requests.post(url=host + "/kyfx/info/login2_ajax.jsp",
                         params={"var1": "admin", "var2": "Ad_123", "var3": ver_code, "type": "1"},
                         headers={"cookie": cookie})
    print(resp.text)
    if "admin" in resp.text:
        print("login success!")
    return cookie


def get_data():
    resp = requests.get(url=host + "/kyfx/info/index.jsp", headers={"cookie": cookie})
    file = open(os.getcwd() + "/ver.txt", "w+")
    file.write(resp.text)
    soup = BeautifulSoup(resp.text)
    div = soup.findAll("div", {"class": "wrapper"})[1]
    i = div.findAll("li")
    print(len(i))
    for index in range(1, len(i)):
        print(i[index].text)


def parse_guider():
    #    file = open("/home/haiyuzhu/Desktop/jq.txt","w+")
    #    resp = requests.post(url= host + "/kyfx/info/jq_manager.jsp?type=1", headers={"cookie":cookie})
    #    file.write(resp.text)
    #    file.close()
    file = open("/home/haiyuzhu/Desktop/jq.txt", "r")
    text = file.read()
    file.close()
    js = json.loads(text)
    for streets in js:
        print("street: " + streets["street"])
        for scene in streets["value"]:
            print("jq_id:   " + scene["jq_id"])
            print("jq_name: " + scene["jq_name"])
            print("street:  " + scene["street"])
            print("type:    " + scene["type"])
            jq_id = scene["jq_id"]
            jq_name = scene["jq_name"]
            jq_type = scene["type"]
            resp = requests.get(usl=host + "/kyfx/info/oldHeader.jsp",
                                headers={"cookie": cookie}, params={"scenicid": jq_id, "position_name": jq_name})


"""
 下载全部景区2015/9/1——2016/9/1 包含江苏剔除南京的31省客流量
"""


def GetQuanShiJingQuKeYuanRanking(dayFrom, dayTo):
    resp = requests.post(url=host + "/kyfx/info/jqkeyuanpaiming.jsp",
                         params={"var": 5, "data": (dayFrom + "---" + dayTo), "outNj": 1},
                         headers={"cookie": cookie})
    resp.raise_for_status()
    time.sleep(random.randint(1, 3))

    Referer = "http://218.94.79.6:8095/kyfx/info/jqkeyuanpaiming.jsp?var=5&data=" + (
    dayFrom + "---" + dayTo) + "&outNj=1"
    resp = requests.post(url=host + "/kyfx/info/jqkeyuanpaiming1.jsp",
                         params={"war": 5, "outNj": 1}, headers={"cookie": cookie, "Referer": Referer})
    resp.raise_for_status()
    time.sleep(random.randint(1, 5))

    Referer = "http://218.94.79.6:8095/kyfx/info/jqkeyuanpaiming1.jsp?war=5&outNj=1"
    resp = requests.post(url=host + "/kyfx/info/xiazai.jsp",
                         params={"var": "jqkeyuan"}, headers={"cookie": cookie, "Referer": Referer})
    resp.raise_for_status()

    file_name = os.getcwd() + "\\" + dayFrom + "--" + dayTo + ".xls";
    file = open(file_name, "wb+")
    file.write(resp.content)
    file.close()


"""
    全市乡村客流排名
"""


def GetQuanShiXiangCunKeYuanRanking(dayFrom, dayTo):
    resp = requests.post(url=host + "/kyfx/info/XiangcunyouKeYuanPaiMing.jsp",
                         params={"var": 5, "data": (dayFrom + "---" + dayTo), "outNj": 1},
                         headers={"cookie": cookie})
    resp.raise_for_status()
    time.sleep(random.randint(1, 3))

    Referer = "http://218.94.79.6:8095/kyfx/info/XiangcunyouKeYuanPaiMing.jsp?var=5&data=" + (
    dayFrom + "---" + dayTo) + "&outNj=1"
    resp = requests.post(url=host + "/kyfx/info/XiangcunyouKeYuanPaiMing1.jsp",
                         params={"war": 5, "outNj": 1}, headers={"cookie": cookie, "Referer": Referer})
    resp.raise_for_status()
    time.sleep(random.randint(1, 2))

    Referer = "http://218.94.79.6:8095/kyfx/info/XiangcunyouKeYuanPaiMing1.jsp?war=5&outNj=1"
    resp = requests.post(url=host + "/kyfx/info/xiazai.jsp",
                         params={"var": "jqkeyuanxcykeyuan"}, headers={"cookie": cookie, "Referer": Referer})
    resp.raise_for_status()

    file_name = os.getcwd() + "\\" + dayFrom + "--" + dayTo + ".xls";
    file = open(file_name, "wb+")
    file.write(resp.content)
    file.close()


"""
# 全市乡村客源，具体到江苏省的地级市
"""


def GetJiangSuCityRanking(dayFrom, dayTo):
    # 包含南京
    day_from = ""
    day_to = ""
    for c in dayFrom:
        if c != '-':
            day_from += c

    for c in dayTo:
        if c != '-':
            day_to += c

    resp = requests.post(url=host + "/kyfx/info/XiangcunyouKeYuanPaiMing.jsp",
                         params={"var": 4, "data": (dayFrom + "---" + dayTo), "outNj": 2},
                         headers={"cookie": cookie})
    resp.raise_for_status()
    time.sleep(random.randint(1, 3))

    resp = requests.post(url=host + "/kyfx/info/XiangcunyouKeYuanPaiMing1.jsp",
                         params={"war": 4, "outNj": 2}, headers={"cookie": cookie})
    resp.raise_for_status()
    time.sleep(random.randint(1, 2))

    form_data = {"a": "江苏", "b": day_from, "c": day_to, "d": 4, "e": 2}

    resp = requests.post(url=host + "/kyfx/info/pAll.jsp",
                         data=form_data,
                         params={"scenictype": 4, "data": (dayFrom + "---" + dayTo)},
                         headers={"cookie": cookie})
    resp.raise_for_status()

    resp = requests.post(url=host + "/kyfx/info/xiazai.jsp",
                         params={"var": "procity"}, headers={"cookie": cookie})
    resp.raise_for_status()
    file_name = os.getcwd() + "\\" + dayFrom + "--" + dayTo + ".xls";
    file = open(file_name, "wb+")
    file.write(resp.content)
    file.close()


def main():
    # print (get_cookie())
    # get_data()
    # parse_guider()
    day = datetime.date(2015, 9, 1)
    dayFrom = day.strftime("%Y-%m-%d")
    dayEnd = datetime.date(2016, 9, 2).strftime("%Y-%m-%d")
    while (dayFrom != dayEnd):
        print(dayFrom)
        GetJiangSuCityRanking(dayFrom, dayFrom)
        day = day + datetime.timedelta(days=1)
        dayFrom = day.strftime("%Y-%m-%d")


"""
    day = datetime.date(2016,4,1)
    dayFrom = day.strftime("%Y-%m-%d")
    dayEnd = datetime.date(2016,9,2).strftime("%Y-%m-%d")
    while (dayFrom != dayEnd):
        print(dayFrom)
        GetQuanShiXiangCunKeYuanRanking(dayFrom, dayFrom)
        day = day + datetime.timedelta(days=1)
        dayFrom = day.strftime("%Y-%m-%d")

"""

"""
# 下载全部景区2015/9/1——2016/9/1 包含江苏剔除南京的31省客流量
    day = datetime.date(2015,9,1)
    dayFrom = day.strftime("%Y-%m-%d")
    dayEnd = datetime.date(2016,9,2).strftime("%Y-%m-%d")
    while (dayFrom != dayEnd):
        print(dayFrom)
        GetQuanShiJingQuKeYuanRanking(dayFrom, dayFrom)
        day = day + datetime.timedelta(days=1)
        dayFrom = day.strftime("%Y-%m-%d")
"""

if __name__ == '__main__':
    main()
