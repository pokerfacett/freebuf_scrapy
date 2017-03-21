#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pymysql
from pymysql.err import InternalError, ProgrammingError
import re
import configparser

# 数据库相关全局变量
host = ""
username = ""
password = ""
dbname = ""

# 配置文件中读取数据库相关信息
def dbinfo_get():
    try:
        conf = configparser.ConfigParser()
        conf.read("config.cfg")
        global host,username,password,dbname
        host = conf.get("database", "host")
        username = conf.get("database", "username")
        password = conf.get("database", "password")
        dbname = conf.get("database", "dbname")
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

# 数据库读取函数，读取文章的title和content，分别与词库中的词进行比对，并将比对结果写入数据库
def db_match():
    conn = db_connect()
    try:
        cur = conn.cursor()
        cur.execute("USE freebuf")
        # 循环取出每篇文章的title和content并进行词库匹配
        cur.execute("SELECT id,title,content FROM scrapy")
        results = cur.fetchall()
        for result in results:
            title_tmp = ""
            content_tmp = ""
            with open("lexicon_final.txt") as file:
                for line  in file:
                    if line.replace("\n","") in result[1]:
                        #print("title: "+line)
                        title_tmp += line.replace("\n","") + ","
                    if line.replace("\n","") in result[2]:
                        #print("content: "+line)
                        content_tmp += line.replace("\n","") + ","
                #print("title: "+title_tmp)
                #print("content: "+content_tmp)
            # 存入数据库
            title_sql = "UPDATE scrapy SET titlematch='"+title_tmp+"',"+"contentmatch='"+content_tmp+"' WHERE id ="+str(result[0])
            cur.execute(title_sql)
            cur.connection.commit()
    except ProgrammingError as e:
        if 1146 == e.args[0]:
            cur.execute("CREATE TABLE IF NOT EXISTS scrapy (Id int primary key auto_increment,title varchar(255),content longtext,time varchar(255),keywords varchar(255),category varchar(255),href varchar(255),artificial varchar(255),automark varchar(255),titlematch varchar(255),contentmatch longtext)")
        else:
            print(e)

if __name__ == "__main__":
    db_match()