#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import configparser
import sys
import pymysql
from pymysql.err import InternalError, ProgrammingError
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import re
import importlib

# 数据库相关全局变量
host = ""
username = ""
password = ""
dbname = ""

# 配置文件中读取据库库相关信息
def dbinfo_get():
    try:
        conf = configparser.ConfigParser()
        conf.read("config.cfg")
        global host,username,password,dbname
        host = conf.get("database", "host")
        username = conf.get("database", "username")
        password = conf.get("database", "password")
        dbname = conf.get("database", "dbname")
        #print "host ip is " + host
        #print "username is " + username
        #print "password is " + password
        #print "dbname is " + dbname
    except configparser.NoSectionError as e:
        print(e)
        sys.exit(1)

# 从配置文件中获取爬取目标根url
def baseurl_get():
    try:
        conf = configparser.ConfigParser()
        conf.read("config.cfg")
        global url
        url = conf.get("web", "url")
        return url
        #print "base url is " + url
    except configparser.NoSectionError as e:
        print(e)
        sys.exit(1)

# 从配置文件中获取freebuf中的子标签
def subtag_get():
    try:
        conf = configparser.ConfigParser()
        conf.read("config.cfg")
        global url
        category = "terminal"
        url = conf.get("target", category)
        if "vuls" == category:
            article_type = "漏洞"
        elif "sectool" == category:
            article_type = "安全工具"
        elif "web" == category:
            article_type = "WEB安全"
        elif "system" == category:
            article_type = "系统安全"
        elif "network" == category:
            article_type = "网络安全"
        elif "wireless" == category:
            article_type = "无线安全"
        elif "terminal" == category:
            article_type = "设备/客户端安全"
        elif "database" == category:
            article_type = "数据库安全"
        elif "management" == category:
            article_type = "安全管理"
        elif "es" == category:
            article_type = "企业安全"
        else:
            article_type = ""
        return url,article_type
    except configparser.NoSectionError as e:
        print(e)
        sys.exit(1)

# 数据库操作，从配置文件中读取待操作数据库名称，数据库密码，并进行链接测试
def db_connect():
    dbinfo_get()
    try:
        global host,username,password,dbname
        conn = pymysql.Connect(host=host,user=username,passwd=password,db=dbname,charset='utf8')
        return conn
    except InternalError as e:
        print(e)
        sys.exit(2)

# 数据库写入函数
def db_store(title,content,time,keyword,category,href,artificial):
    conn = db_connect()
    try:
        cur = conn.cursor()
        cur.execute("USE freebuf")
        cur.execute("INSERT INTO scrapy (title,content,time,keywords,category,href,artificial) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")", (title,content,time,keyword,category,href,artificial))
        cur.connection.commit()
    except ProgrammingError as e:
        if 1146 == e.args[0]:
            cur.execute("CREATE TABLE IF NOT EXISTS scrapy (Id int primary key auto_increment,title varchar(255),content longtext,time varchar(255),keywords varchar(255),category varchar(255),href varchar(255),artificial varchar(255))")
            #cur.execute("CREATE TABLE IF NOT EXISTS pages (Id int primary key auto_increment,href varchar(255))")
        else:
            print(e)
# 这里可以用多线程同时处理，为了测试，暂时只用一个标签

# 爬取文章对应url内容、文章布时间、文章关键词
def article_scrap(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print(e)
        sys.exit(3)
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        # 返回文章内容
        content = bsObj.find("div",{"id":"contenttxt"}).get_text()
        # 返回文章创建时间
        times = bsObj.findAll("div",{"class":"property"})
        for time in times:
            finaltime = time.find("span",{"class","time"}).get_text()
            #print(finaltime)
        # 文章关键词
        keyword = bsObj.find("meta",{"name":"keywords"}).get("content")
        #print(keyword)
        return content,finaltime,keyword
    except AttributeError as e:
       print(e)
       return None

# 爬虫函数，爬取freebuf上的文章
def freebuf_scrap():
    suburl,article_type = subtag_get()
    baseurl = baseurl_get()
    url_scrap = baseurl + suburl
    # print("url is " + url_scrap)
    try:
        html = urlopen(url_scrap)
    except (HTTPError, URLError) as e:
        print(e)
        sys.exit(3)
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        #print(bsObj.findAll("div",{"class":"news-info"}))
        namelist = bsObj.findAll("div",{"class":"news-info"})
        #print(namelist[1].find("a",href=re.compile("^"+url_scrap+"[0-9]{6,}\.html$")).get('title'))
        for name in namelist:
            # 得到整个数据
            #print(name.find("a"))
            # 得到title
            #print(name.find("a").get("title"))
            article_title = name.find("a").get("title")
            # 得到url
            #print(name.find("a").get("href"))
            article_href = name.find("a").get("href")
            # 访问指定页面,并下载对应的网页内容,并获取文章时间及关键词
            article_content,article_time,article_keywords = article_scrap(article_href)
            #print(article_content)
            #print(article_time)
            #print(article_keywords)

            # 将信息写入数据库，包括：题目、文章内容、创建时间、关键词、文章大分类、文章链接、人工标注的标签
            db_store(article_title,article_content,article_time,article_keywords,article_type,article_href,"")
            
    except AttributeError as e:
        print(e)
        sys.exit(3)


freebuf_scrap()