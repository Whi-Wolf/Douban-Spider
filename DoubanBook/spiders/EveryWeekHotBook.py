import scrapy
from os import remove
import os
from DoubanBook.items import DoubanBookItem
import shutil
import stat
import re
import jieba
import jieba.analyse
from bs4 import BeautifulSoup as bs
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud, STOPWORDS #词云包
import matplotlib.pyplot as plt
import urllib
from urllib import request


class EveryweekhotbookSpider(scrapy.Spider):
    name = "EveryWeekHotBook"
    allowed_domains = ["book.douban.com"]
    start_urls =  ["https://book.douban.com/"]
    

    #清除一下目录
    try:
        remove('book.doc')
    except:
        pass
    
    try:
        os.chmod(r'D:\Anaconda\DoubanBook\DoubanBook\Img', stat.S_IWUSR)#修改文件权限
        shutil.rmtree(r'D:\Anaconda\DoubanBook\DoubanBook\Img')  #递归删除文件夹
    except:
        pass
    
    try:
        os.chmod(r'D:\Anaconda\DoubanBook\DoubanBook\wordcloud', stat.S_IWUSR)#修改文件权限
        shutil.rmtree(r'D:\Anaconda\DoubanBook\DoubanBook\wordcloud')  #递归删除文件夹
        os.mkdir('./wordcloud')
    except:
        pass
    


    
    def parse(self, response):
        #定位热书榜     
        selector=response.xpath('//div[@class="section popular-books"]')
        for book in selector.xpath('.//li[@class=""]'):
            bookname=book.xpath('.//h4[@class="title"]/a/text()').extract_first()
            author=book.xpath('.//p[@class="author"]//text()').extract_first()
            pic=book.xpath('.//img/@src').extract_first()
            bookurl=book.xpath('.//a/@href').extract_first()
            
            #print(bookurl)
            commentList = []
            #评论前10页，如果少于10页，返回空列表喽
            for i in range(10): 
                pageNum = i + 1
                eachCommentList = [];
                if pageNum>0:
                    start = (pageNum-1) * 20
                else:
                    return False
                bookid=re.search('[0-9]{8,10}',str(bookurl)).group(0)
                requrl = 'https://book.douban.com/subject/' + bookid + '/reviews?start='  + str(start) 
                #print(requrl)
                
                # headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5' ,
                #          'Referer':requrl,
                #          'Connection':'keep-alive'}
                #header会崩不知道为啥（可能是请求太频繁）
                headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
                #开始用beautifulsoup了！
                request2 = urllib.request.Request(requrl,headers=headers)
                esp = urllib.request.urlopen(request2)
                html_data = esp.read().decode('utf-8')   
                soup = bs(html_data, 'html.parser')
                comment_div_lits = soup.find_all('div', class_='review-list')
                #print(comment_div_lits[0])
                for item in comment_div_lits:
                    #print(item.find_all(‘p’))
                    p=item.find_all('div',class_='short-content')
                    print(p)
                    if p != []:
                        p=p[0].text
                        eachCommentList.append(p)
                    else:break
                commentList.append(eachCommentList)
            #将列表中的数据转换为字符串
            comments = ''
            for k in range(len(commentList)):
                comments = comments + (str(commentList[k])).strip()
            #使用正则表达式去除标点符号
            pattern = re.compile(r'[\u4e00-\u9fa5]+')
            filterdata = re.findall(pattern, comments)
            cleaned_comments = ''.join(filterdata)
            #使用结巴分词进行中文分词
            result=jieba.analyse.textrank(cleaned_comments,topK=50,withWeight=True)
            keywords = dict()
            for i in result:
                keywords[i[0]]=i[1]    
            
            #停用词集合
            stopwords = set(STOPWORDS)
            f=open('./StopWords.txt',encoding="utf8")
            while True:
                word=f.readline()
                if word=="":
                    break
                stopwords.add(word[:-1])

            keywords={ x:keywords[x] for x in keywords if x  not in stopwords}
            print("\n删除停用词后",keywords)
            #用词云进行显示
            wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",
            max_font_size=80,stopwords=stopwords)
            word_frequence=keywords
            myword=wordcloud.fit_words(word_frequence)
            myword.to_file(r'./wordcloud/'+bookname+'词云图.jpg')  # 将词云图保存到指定文件夹(指定文件夹要是已经存在的)
            # plt.imshow(myword)#展示词云图
            # plt.axis("off")
            # plt.show() 
            
            
            item =DoubanBookItem()
            item['bookname']=bookname
            item['author']=author
            item['image_urls']=pic
            yield item
    
    
       