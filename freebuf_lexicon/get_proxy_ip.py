#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#from bs4 import BeautifulSoup
from urllib.request import urlopen,ProxyHandler,build_opener,install_opener,Request,HTTPHandler
from urllib.error import HTTPError,URLError
import socket
# 验证代理ip是否可用
def check_proxy(proxy_ip):
    proxy = {"http:":"http://"+proxy_ip}
    proxy_handler = ProxyHandler(proxy)
    opener = build_opener(HTTPHandler,proxy_handler)
    install_opener(opener)
    request = Request("http://www.freebuf.com/?action=ajax_wenku&year=all&score=all&type=all&tech=0&keyword=&page=1")
    try:
        html = urlopen(request, data=None, timeout=3)
        print(html.read())
        return True
    except (HTTPError,URLError) as e:
        print(e)
        return False
    except socket.timeout as e:
        print(e)
        return False 
    
proxy_ip = []
with open("500_proxy.txt","rt") as f:
    for line in f:
        #dict = dict.fromkeys(tmp,"http://"+line)
        dict = {"http:":"http://"+line.replace("\n","")}
        #check_proxy(line.replace("\n", ""))
        if check_proxy(line.replace("\n", "")):
            proxy_ip.append(dict)
        else:
            pass
    print(proxy_ip)


with open("proxyIP_5.py","wt") as f:
    f.write("#!/usr/bin/python3\n#-*-coding:utf-8-\nproxy_list=[")
    for line in proxy_ip:
        f.write(str(line))
        f.write(",\n")
    f.write("]")