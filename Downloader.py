# -*- coding: utf-8 -*-

"""
Created on  2016/10/23
Author:     Haiyu Zhu
E-mail:     zhuhaiyu1991@163.com
"""

import requests
import os


class Downloader(object):

    def __init__(self, **kwargs):
        if "cookie" in kwargs:
            self.cookie = kwargs["cookie"]
        else:
            self.cookie = ""

        if "host" in kwargs:
            self.host = kwargs["host"]
        else:
            self.host = "http://218.94.79.6:8095"

        if "user_name" in kwargs:
            self.user_name = kwargs["user_name"]
        else:
            self.user_name = "admin"

        if "pass_word" in kwargs:
            self.pass_word = kwargs["pass_word"]
        else:
            self.pass_word = "Ad_321"

        if "work_dir" in kwargs:
            self.work_dir = kwargs["work_dir"]
        else:
            self.work_dir = os.getcwd()

    def login(self, related_path="/kyfx/info/login.jsp"):
        resp = requests.get(url=self.host + related_path)
        resp.raise_for_status()
        self.cookie = resp.headers["set-cookie"]

        resp = requests.get(url=self.host + "/kyfx/info/yanzhengma.jsp", headers={"cookie":self.cookie})
        resp.raise_for_status()

        if not os.path.exists(self.work_dir + "\\temp"):
            os.mkdir(self.work_dir + "\\temp")

        file = open(self.work_dir + "\\temp\\ver.jpg", "wb+")
        file.write(resp.content)
        file.close()

        ver_code = input("验证码：")
        resp = requests.post(url=self.host + "/kyfx/info/login2_ajax.jsp",
                             params={"var1":self.user_name, "var2":self.pass_word, "var3":ver_code, "type": "1"},
                             headers={"cookie": self.cookie})
        resp.raise_for_status()
        file = open(self.work_dir + "\\temp\\cookie.txt", "w+")
        file.write(self.cookie)
        file.close()
        if "admin" in resp.text:
            print("login successfully!")
            return True
        else:
            print("login failed! \nYou may check the user name, password and cookie!")
            return False

    def set_cookie(self, cookie_path="\\temp\\cookie.txt"):
        file = open(self.work_dir + cookie_path, mode="r")
        self.cookie = file.read()
        file.close()
        print("Read cookie:", self.cookie)

    def fetch_data(self, **kwargs):
        pass

    def process_data(self, **kwargs):
        pass

    def pipeline(self, **kwargs):
        self.login()
        self.fetch_data()
        self.process_data()


if __name__ == "__main__":
    downloader = Downloader()
    downloader.set_cookie()

