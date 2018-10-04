# -*- coding: utf-8 -*-
import urllib.request
import json
import pymongo
from db import save_content
import re

#id='2360812967'#可以通过昵称查找id
count = 0
scraw_ID = set(['2360812967',])#待爬id
finish_ID = set()#已爬id 120.79.245.47
weibocount = 0

proxy_addr="122.241.72.191:808"

def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

def get_containerid(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    print('get_containerid')
    if content.get('tabsInfo') is not None:
        for data in content.get('tabsInfo').get('tabs'):
            if(data.get('tab_type')=='weibo'):
                containerid=data.get('containerid')
                return containerid
    else:
        print('containerid is None!')

def get_lfid(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    #content=json.loads(data).get('data')
    result=re.search('lfid=.*?(\d+)',data,re.S)
    if result:
        containerid = result.group(1)
        return containerid


def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')  
    urank=content.get('userInfo').get('urank')
    print("name:"+name+"\n"+"profile_url:"+profile_url+"\n"+"profile_image_url:"+profile_image_url+"\n"+"verified:"+str(verified)+"\n"+"description:"+description+"\n"+"guanzhu:"+str(guanzhu)+"\n"+"fensi:"+str(fensi)+"\n"+"gender:"+gender+"\n"+"urank:"+str(urank)+"\n")


def get_weibo(id,file):    
    i=1
    global weibocount
    containerid = get_containerid(id)
    if containerid is not None:
        while True:
            #url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
            weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+containerid+'&page='+str(i)
            #guanzhu_url = 'https://m.weibo.cn/api/container/getSecond?containerid='+get_containerid(id)+'_-_FOLLOWERS&page='+str(i)
            try:
                data=use_proxy(weibo_url,proxy_addr)
                content=json.loads(data).get('data')
                cards=content.get('cards')
                if(len(cards)>0):
                    for item in get_weibo_content(content,id):
                        weibocount+=1
                        save_content(item)#以后可以考虑存储图片url
                    i+=1
                else:
                    break

                '''
                cards=content.get('cards')
                print("-----No"+str(i)+"page------")
                if(len(cards)>0):
                    
                    for j in range(len(cards)):
                        #print("-----No"+str(i)+"page,No"+str(j)+"weibo------")
                        global count
                        count+=1
                        print(count)
                        card_type=cards[j].get('card_type')
                        if(card_type==9):
                            mblog=cards[j].get('mblog')
                            mblog_id = mblog.get('id')
                            attitudes_count=mblog.get('attitudes_count')
                            comments_count=mblog.get('comments_count')
                            created_at=mblog.get('created_at')
                            reposts_count=mblog.get('reposts_count')
                            scheme=cards[j].get('scheme')
                            text=mblog.get('text')
                            
                            with open(file,'a',encoding='utf-8') as fh:
                                fh.write("----No"+str(i)+"page,No"+str(j)+"weibo----"+"\n")
                                #fh.write("weibo addr:"+str(scheme)+"\n"+"sub time:"+str(created_at)+"\n"+"sub content:"+text+"\n"+"attitudes_count:"+str(attitudes_count)+"\n"+"comments_count:"+str(comments_count)+"\n"+"reposts_count:"+str(reposts_count)+"\n")
                                fh.write("weibo addr:"+str(scheme)+"\n"+"sub time:"+str(created_at)+"\n"+"sub content:"+text+"\n")
                            
                            
                            #-----------------------------------------------------------------
                            
                            k = 1
                            single_weibo_url='https://m.weibo.cn/api/comments/show?id='+mblog_id+'&page='+str(k)
                            try:
                                data1=use_proxy(single_weibo_url,proxy_addr)
                                #print(data1)
                                is_ok=json.loads(data1).get("ok")   
                                #print(is_ok)
                                if is_ok==1:
                                    
                                    content1=json.loads(data1).get('data')   
                                    data=content1.get('data')
                                    for l in range(len(data)):
                                        comment = data[l].get('text')
                                        with open(file,'a',encoding='utf-8') as fh:
                                            fh.write("------------------------comment------------------"+"\n")
                                            fh.write("weibo comment:"+str(comment)+"\n")
                                    
                            except Exception as e:
                                print(e)
                                pass
                
                    
                    #i+=1   
                else:
                    break
            '''
            except Exception as e:
                print(e)
                pass
        print('the weibocount is:'+str(weibocount))
        
def get_weibo_content(content,id):
    for cards in content.get('cards'):        
        card_type=cards.get('card_type')
        if(card_type==9):
            mblog=cards.get('mblog')
            #mblog_id = mblog.get('id')
            #attitudes_count=mblog.get('attitudes_count')
            #comments_count=mblog.get('comments_count')
            created_at=mblog.get('created_at')
            #reposts_count=mblog.get('reposts_count')
            #scheme=cards.get('scheme')
            text=mblog.get('text')
            text=re.sub('<.*>','',text)
            
            yield {
                'user_id':id,
                'time':created_at,
                'text':text,
            }

def expand_id_pool(id):
    i =1
    lfid = get_lfid(id)
    if lfid is not None:
        while(True):
            #url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
            guanzhu_url = 'https://m.weibo.cn/api/container/getSecond?containerid='+lfid+'_-_FOLLOWERS&page='+str(i)
            try:
                data=use_proxy(guanzhu_url,proxy_addr)
                content=json.loads(data).get('data')
                #print(content)
                if content.get('cards') is not None:
                    for cards in content.get('cards'):   
                        #print(i)     
                        card_type=cards.get('card_type')
                        if(card_type==10):
                            user=cards.get('user')
                            user_id = user.get('id')
                            if user_id not in finish_ID:
                                scraw_ID.add(str(user_id))
                    #print(i)
                    i+=1
                else:
                    break
            except Exception as e:
                print(e)
                pass
        


if __name__=="__main__":
    idnum = 0
    while(True):
        while scraw_ID.__len__():
            #print(scraw_ID.__len__())
            idnum+=1
            id = scraw_ID.pop()
            finish_ID.add(id)
            print('the id is '+ id)
            expand_id_pool(id)
            #print('the id num is '+ str(idnum))

            file=id+".txt"        
            get_weibo(id,file)

