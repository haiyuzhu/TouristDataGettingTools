# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:54:57 2016

@author: haiyuzhu
"""

import requests
import json
from bs4 import BeautifulSoup
import tablib  

host = "http://218.94.79.6:8095"
cookie = "JSESSIONID=DCE921E6A331C69CE418B1A3FEF3B4ED"
    
    
def get_cookie():
    resp = requests.get(url=host + "/kyfx/info/login.jsp")
    cookie = resp.headers['set-cookie']
    resp = requests.get(url=host + "/kyfx/info/yanzhengma.jsp", headers={"cookie" : cookie})
    
    file = open("/home/haiyuzhu/Desktop/ver.jpg", "wb+")
    file.write(resp.content)
    file.close()
    ver_code = raw_input()
    resp = requests.post(url=host+"/kyfx/info/login2_ajax.jsp", 
                         params = {"var1":"admin","var2":"Ad_123","var3":ver_code,"type":"1"},
                         headers={"cookie" : cookie})
    print resp.text    
    if "admin" in resp.text:
        print "login success!"
    return cookie

def get_data():

    resp = requests.get(url=host+"/kyfx/info/index.jsp", headers={"cookie" : cookie})
    file = open("/home/haiyuzhu/Desktop/ver.txt","w+")
    file.write(resp.text)    
    soup = BeautifulSoup(resp.text)
    div = soup.findAll("div",{"class":"wrapper"})[1]
    i = div.findAll("li")
    print len(i)
    for index in range(1,len(i)):
        print i[index].text
        
def parse_guider():
#    file = open("/home/haiyuzhu/Desktop/jq.txt","w+")
#    resp = requests.post(url= host + "/kyfx/info/jq_manager.jsp?type=1", headers={"cookie":cookie})
#    file.write(resp.text)
#    file.close()
    file = open("/home/haiyuzhu/Desktop/jq.txt","r")
    text = file.read()
    file.close()    
    js = json.loads(text)
    for streets in js:
        print "street: " + streets["street"]
        for scene in streets["value"]:
            print "jq_id:   " + scene["jq_id"]
            print "jq_name: " + scene["jq_name"]
            print "street:  " + scene["street"]
            print "type:    " + scene["type"]
            jq_id = scene["jq_id"]
            jq_name = scene["jq_name"]
            jq_type = scene["type"]
            resp = requests.get(usl = host + "/kyfx/info/oldHeader.jsp",
                                hearder={"cookie":cookie}, params = {"scenicid":jq_id, "position_name":jq_name, })
            
    
    
def main():
    #get_data()
    parse_guider()


main()
