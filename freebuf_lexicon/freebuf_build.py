#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib.request import urlopen,ProxyHandler,build_opener,install_opener,Request,HTTPHandler
from urllib.error import HTTPError,URLError
import urllib
from bs4 import BeautifulSoup
import math
import threading
import proxyIP_5
import user_agents_1
import random
import time
import socket
from http.client import IncompleteRead,HTTPException

# 遍历freebuf文章的url,最后的page是页数，目前是从1-865
freebuf_url = "http://www.freebuf.com/?action=ajax_wenku&year=all&score=all&type=all&tech=0&keyword=&page="
# 词库文件
lexicon = "lexicon.txt"
# 页数，从1=865页，初始是1页，意思是从最新的开始爬，终止是865页
pages = 856
# 定义线程锁
thread_lock = threading.Lock()
# 定义线程列表
thread_list = []

# 定义线程类
class scrapy_thread (threading.Thread):
    def __init__(self, threadID, pageinit, pagefinal):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.pageinit = pageinit
        self.pagefinal = pagefinal
    def run(self):
        keywords_page_scrapy(self.pageinit,self.pagefinal)

# 使用代理访问url
def proxy_urlopen(url):
    proxy = random.choice(proxyIP_5.proxy_list)
    #proxy = {"http:":"http://186.46.57.90:8080"}
    proxy = random.choice(proxyIP_5.proxy_list)
    proxy_handler = ProxyHandler(proxy)
    opener = build_opener(HTTPHandler,proxy_handler)
    install_opener(opener)
    request = Request(url)
    #user_agent = random.choice(user_agents_1.user_agents)
    #request.add_header('User-Agent',user_agent)
    time.sleep(5)
    try:
        print(url)
        html = urlopen(request, data=None, timeout=10)
        return html
    except (HTTPError,URLError,socket.timeout,socket.error,HTTPException) as e:
        print(e)
        return

# 正常访问url，为了防止ip被封，爬得慢一些
def nomal_urlopen(url):
    html = urlopen(url)
    time.sleep(5)
    return html

# 爬取每一页中文章的所有url
def page_scrapy(url):
    final_urls = []
    html = proxy_urlopen(url)
    #html = nomal_urlopen(url)
    # print(html.read())
    if html == None:
        return
    # print(html.read().decode('unicode-escape'))
    try:
        bsObj = BeautifulSoup(html.read().decode('unicode-escape'),"html5lib")
        # 爬取本页所有的文章链接并返回url
        all_url = bsObj.findAll("div",{"class":"article-text"})
        for one_url in all_url:
            # final_urls.append()
            # final_url = one_url.find("h3").find("a").get("href").replace("\\","")
            # print(final_url)
            final_urls.append(one_url.find("h3").find("a").get("href").replace("\\",""))
        # print(final_urlsi)
        return final_urls
    except AttributeError as e:
        print(e)
        print("pages")
        return
    
# 爬取文章的关键词，并写入文件
def keyword_scrapy(url):
    html = proxy_urlopen(url)
    if html == None:
        return
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        # 文章关键词
        keywords = bsObj.find("meta",{"name":"keywords"}).get("content").split(",")
        print(keywords)
        for keyword in keywords:
            if keyword == "":
                break
            else:
                with open(lexicon, 'at') as f:
                   f.write(keyword+'\n') 
    except (AttributeError,socket.timeout,socket.error,IncompleteRead,HTTPException,URLError) as e:
        print(e)
        return

# 爬取某几页中所有页面的关键词,为了采用多线程
def keywords_page_scrapy(pageinit,pagefinal):
    global freebuf_url
    for page in range(pageinit,pagefinal+1):
        print("Page is" + str(page))
        print("Page init is"+ str(pageinit))
        print("Page final is"+ str(pagefinal))
        url = freebuf_url + str(page)
        final_urls = page_scrapy(url)
        try:
            for final_url in final_urls:
                # 因为需要对文件进行写，因此需要加锁
                thread_lock.acquire() 
                keyword_scrapy(final_url)
                thread_lock.release()
                #time.sleep(5)
        except TypeError as e:
            print (e)
            continue

if __name__ == '__main__':
    # 多线程，每100个页面开一个线程
    thread_num = math.ceil(pages / 100)
    for thread in range (1,thread_num+1):
        if thread == thread_num:
            #keywords_page_scrapy((thread-1)*100,pages)
            thread_list.append(scrapy_thread(thread,(thread-1)*100,pages))
        elif thread == 1:
            #keywords_page_scrapy(1,thread*100-1)
            thread_list.append(scrapy_thread(thread,1,thread*100-1))
        else:
            #keywords_page_scrapy((thread-1)*100,thread*100-1)
            thread_list.append(scrapy_thread(thread,(thread-1)*100,thread*100-1))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    #keywords_page_scrapy(1,9)
    print("Scrapy has finished!!!!")