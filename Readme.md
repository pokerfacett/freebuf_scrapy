# freebuf文件夹介绍
## freebuf_article文件夹
爬取freebuf上的文章，并存入数据库
- **config.cfg**
    
    配置文件，配置了数据库信息和爬虫的信息
- **freebuf_scrapy.py**

    爬虫文件，爬取freebuf的文章，分类由配置文件读取，每个分类只爬一页的内容，并将爬取的内容存入数据库。由于爬的内容较少，因此未设置代理，且是单线程的
    
## **freebuf_lexicon文件夹**
爬取freebuf所有文章的关键词，并作为词库，采用代理ip，多线程
- 500_proxy.txt

    网上找的代理ip池，但是不一定都存活，代理ip网址：
    http://www.66ip.cn/nm.html 
- get_proxy_ip.py

    检测代理ip是否存活，并过滤出可用的代理ip供使用，最终形成proxyIP_5.py，可直接import
    
- proxyIP_5.py

    活动的代理ip地址池
    
- freebuf_build.py

    爬取关键词，采用代理ip，多线程
- lexicon.txt

    爬取到的关键词词库
    
- user_agents_1.py
 
    浏览器代理，可直接import
## **freebuf_lexicon_handle**文件夹
- lexicon_handle.py
	
	对爬取的词库进行预处理，去掉空格等，形成lexicon_final.txt词库
- lexicon_final.txt
	
	最终形成的词库
- test.txt
	
	爬取的未处理的词库
- lexicon_match.py
	
	将文章的标题和内容进行词库查询与匹配
- config.cfg
	
	数据库配置文件