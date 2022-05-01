# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:04:34 2020

@author: USER
"""
import sys
import requests
from bs4 import BeautifulSoup
import time

def control():
    x=sys.argv[1]
    if x == "":
        print("Error")
        exit (0)
    if x == 'crawl':
        crawl()
    elif x == 'push':
        y=int(sys.argv[2])
        z=int(sys.argv[3])
        tt = time.time()
        push(y,z)
    elif x == 'popular':
        y=int(sys.argv[2])
        z=int(sys.argv[3])
        popular(y,z)
    elif x == 'keyword':
        y=str(sys.argv[2])
        z=int(sys.argv[3])
        w=int(sys.argv[4])
        keyword(y,z,w)
    else:
        print("Error")
        exit (0) 

def read_page(url,rs):
    content = rs.get(url=url)
    soup = BeautifulSoup(content.text,'html.parser')
    data_list = soup.find_all(class_="r-ent")
    return soup , data_list
    
def change_page(url,soup):
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href
    url = next_page_url
    return url

def takeSecond(elem):
    return elem[1]

def crawl():
    payload = { 'from':'/bbs/Beauty/index.html','yes': 'yes' }
    rs = requests.session()
    res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
    url='https://www.ptt.cc/bbs/Beauty/index.html'

    inform_list = []
    popular_list = []
    
    

    soup,data_list = read_page(url,rs)
    url = change_page(url,soup)
    soup,data_list = read_page(url,rs)
    i = len(data_list)-1

    time_new = 1231
    year = 2020

    while year>2018:
        
        if i<0:
            url = change_page(url,soup)
            soup,data_list = read_page(url,rs)
            i = len(data_list)-1
    
        time_old = int(str(data_list[i].find_all(class_="date")[0].string)[:-3]+str(data_list[i].find_all(class_="date")[0].string)[-2:])
        if time_old > time_new:
            year-=1
        time_new = time_old
        
        if year == 2019 and i>=0:
            if ("刪除" not in str(data_list[i].find_all(class_='title')[0])) and ("[公告]" not in str(data_list[i].find_all(class_='title')[0])):
                inform=''
                title = data_list[i].find_all('a')[0].string
                href = data_list[i].find_all('a')[0].get('href')
                time_tag = str(data_list[i].find_all(class_="date")[0].string)[:-3]+str(data_list[i].find_all(class_="date")[0].string)[-2:]
                
                if time_tag[0]==' ':
                    time_tag=time_tag[1:]
                inform = (time_tag,title,'https://www.ptt.cc'+href)
                print(inform)

                inform_list.append(inform)
                if str(data_list[i].find_all(class_='nrec')[0].string)=="爆":
                    popular_list.append(inform)
        i-=1
    
        time.sleep(0.001)
        print(time_old)
        print(i)
    f=open(r'./all_articles.txt','w',encoding="utf-8")
    length=len(inform_list)-1
    for i in range(len(inform_list)):
        f.write(str(inform_list[length-i][0])+','+str(inform_list[length-i][1])+','+str(inform_list[length-i][2])+'\n')
        print(i)
    f.close()
    length=len(popular_list)-1
    f=open(r'./all_popular.txt','w',encoding="utf-8")
    for i in range(len(popular_list)):
        f.write(str(popular_list[length-i][0])+','+str(popular_list[length-i][1])+','+str(popular_list[length-i][2])+'\n')
        print(i)
    f.close()
    return 0

def push(start_date,end_date):
    
    article_url_list=[]

    f=open(r'./all_articles.txt','r',encoding="utf-8")
    for line in f:
        inform = line.split(',')
        if int(inform[0])>=int(start_date) and int(inform[0])<=int(end_date):
            article_url_list.append(inform[-1][:-1])
        elif int(inform[0])>int(end_date):
            break
    f.close()

    like=[]
    boo=[]
    all_like=0
    all_boo=0
    payload = { 'from':'/bbs/Beauty/index.html','yes': 'yes' }
    rs = requests.session()
    res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
    for article_url in article_url_list:
        time.sleep(0.01)
        url = article_url
        content = rs.get(url=url)
        soup = BeautifulSoup(content.text,'html.parser')
        data_list = soup.find_all(class_="push")
        for i in range(len(data_list)):
            if data_list[i].find_all('span')[0].string=='推 ':
                like.append(str(data_list[i].find_all('span')[1].string))
            elif data_list[i].find_all('span')[0].string=='噓 ':
                boo.append(str(data_list[i].find_all('span')[1].string))
        print(url)         
                
    all_like = len(like)
    all_boo = len(boo)

    like.sort()
    boo.sort()

    like_number=[1]
    like_name=[like[0]]
    like_list=[]
    boo_number=[1]
    boo_name=[boo[0]]
    boo_list=[]
    j=0
    k=0

    for i in range(len(like)-1):
        if like[i]==like[i+1]:
            like_number[i-k]+=1
            k+=1
        else:
            like_name.append(like[i+1])
            like_number.append(1)

    for i in range(len(boo)-1):
        if boo[i]==boo[i+1]:
            boo_number[i-j]+=1
            j+=1
        else:
            boo_name.append(boo[i+1])
            boo_number.append(1)

    like_list = list(zip(like_name,like_number))
    boo_list = list(zip(boo_name,boo_number))
    
    like_list.sort(key=takeSecond,reverse=True)
    boo_list.sort(key=takeSecond,reverse=True)
    
    f= open(r'./push['+str(start_date)+'-'+str(end_date)+'].txt','w',encoding="utf-8")
    f.write('all like: '+str(all_like)+'\n')
    f.write('all boo: '+str(all_boo)+'\n')
    x1 = 0

    while x1<10:
        grade = x1+1
        f.write('like #'+str(grade)+': '+like_list[x1][0]+' '+str(like_list[x1][1])+'\n')
    
        x1+=1
    
        if x1+2>len(like_list) and like_list[x1][1]==like_list[x1-1][1]:
            f.write('boo #'+str(grade)+': '+like_list[x1][0]+' '+str(like_list[x1][1])+'\n')
            break
    
    x1 = 0

    while x1<10:
        grade = x1+1
        f.write('boo #'+str(grade)+': '+boo_list[x1][0]+' '+str(boo_list[x1][1])+'\n')

        x1+=1
    
        if x1+2>len(boo_list) and boo_list[x1][1]==boo_list[x1-1][1]:
            f.write('boo #'+str(grade)+': '+boo_list[x1][0]+' '+str(boo_list[x1][1])+'\n')
            break   
    f.close()    
    return 0

def popular(start_date,end_date):
    article_url_list=[]

    f=open(r'./all_popular.txt','r',encoding="utf-8")
    for line in f:
        inform = line.split(',')
        if int(inform[0])>=int(start_date) and int(inform[0])<=int(end_date):
            article_url_list.append(inform[-1][:-1])
        elif int(inform[0])>int(end_date):
            break
    f.close()
    f= open(r'./popular['+str(start_date)+'-'+str(end_date)+'].txt','w',encoding="utf-8")
    f.write('number of popular articles: '+str(len(article_url_list))+'\n')
    herf_list=[]
    payload = { 'from':'/bbs/Beauty/index.html','yes': 'yes' }
    rs = requests.session()
    res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
    for article_url in article_url_list:
        time.sleep(0.01)
        url = article_url
        content = rs.get(url=url)
        soup = BeautifulSoup(content.text,'html.parser')
        data_list = soup.find_all("a")
        for i in range(len(data_list)):
            if data_list[i].get('href')[-4:]=='.jpg' or data_list[i].get('href')[-4:]=='.png' or data_list[i].get('href')[-4:]=='jpeg' or data_list[i].get('href')[-4:]=='.gif' or data_list[i].get('href')[-4:]=='.JPG' or  data_list[i].get('href')[-4:]=='.PNG' or data_list[i].get('href')[-4:]=='JPEG' or data_list[i].get('href')[-4:]=='.GIF':
                #herf_list.append(data_list[i].get('href'))
                f.write(str(data_list[i].get('href'))+'\n')
    f.close()
    
def keyword(keyword,start_date,end_date):
    article_url_list=[]
    catch_list=[]

    f=open(r'./all_articles.txt','r',encoding="utf-8")
    for line in f:
        inform = line.split(',')
        if int(inform[0])>=int(start_date) and int(inform[0])<=int(end_date):
            article_url_list.append(inform[-1][:-1])
        elif int(inform[0])>int(end_date):
            break
    f.close()

    payload = { 'from':'/bbs/Beauty/index.html','yes': 'yes' }
    rs = requests.session()
    res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
    for url in article_url_list:
        time.sleep(0.01)
        content = rs.get(url=url)
        soup = BeautifulSoup(content.content,'html.parser')
        check_word='※ 發信站'
        string=''
        stop=0
        for i in range(len(soup.text)):
    
            for j in range(len(check_word)):
                if soup.text[i+j]!=check_word[j]:
                    break
                if j==(len(check_word)-1):
                    stop=1
                    string = soup.text[:i-4]

            if stop==1:
                break

        catch=0
        stop=0
        for i in range(len(string)):
            for j in range(len(keyword)):
                if soup.text[i+j]!=keyword[j]:
                    break
                if j==(len(keyword)-1):
                    stop=1
                    catch=1
            if stop==1:
                break

        if catch==1:
            catch_list.append(url)
            
    f= open(r'./keyword('+keyword+')['+str(start_date)+'-'+str(end_date)+'].txt','w',encoding="utf-8")
    herf_list=[]
    payload = { 'from':'/bbs/Beauty/index.html','yes': 'yes' }
    rs = requests.session()
    res = rs.post("https://www.ptt.cc/ask/over18", data=payload)
    for article_url in catch_list:
        time.sleep(0.01)
        url = article_url
        content = rs.get(url=url)
        soup = BeautifulSoup(content.text,'html.parser')
        data_list = soup.find_all("a")
        for i in range(len(data_list)):
            if data_list[i].get('href')[-4:]=='.jpg' or data_list[i].get('href')[-4:]=='.png' or data_list[i].get('href')[-4:]=='jpeg' or data_list[i].get('href')[-4:]=='.gif' or data_list[i].get('href')[-4:]=='.JPG' or  data_list[i].get('href')[-4:]=='.PNG' or data_list[i].get('href')[-4:]=='JPEG' or data_list[i].get('href')[-4:]=='.GIF':
                #herf_list.append(data_list[i].get('href'))
                f.write(str(data_list[i].get('href'))+'\n')
    f.close()
    
    return 0

if __name__ == '__main__':
	control()