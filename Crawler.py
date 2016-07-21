# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:54:57 2016

@author: haiyuzhu
"""

import requests
from bs4 import BeautifulSoup

host = "http://218.94.79.6:8095"
def get_cookie():
    resp = requests.get(url=host + "/kyfx/info/login.jsp")
    cookie = resp.headers['set-cookie']
    resp = requests.get(url=host + "/kyfx/info/yanzhengma.jsp", headers={"cookie" : cookie})
    
    file = open("/home/haiyuzhu/Desktop/ver.jpg", "wb+")
    file.write(resp.content)
    file.close()
    ver_code = raw_input()
    resp = requests.post(url=host+"/kyfx/info/login2_ajax.jsp", params = {"var1":"admin","var2":"Ad_123","var3":ver_code,"type":"1"},headers={"cookie" : cookie})
    print resp.text    
    if "admin" in resp.text:
        print "login success!"
    return cookie

def get_data():
    cookie = "JSESSIONID=E4A5318E7DBB89C41FCE84B767D762F8"
    resp = requests.get(url=host+"/kyfx/info/index.jsp", headers={"cookie" : cookie})
    file = open("/home/haiyuzhu/Desktop/ver.txt","w+")
    file.write(resp.text)    
    soup = BeautifulSoup(resp.text)
    div = soup.findAll("div",{"class":"wrapper"})[1]
    i = div.findAll("li")
    print len(i)
    for index in range(1,len(i)):
        print i[index].text

def main():
    get_data()


main()
