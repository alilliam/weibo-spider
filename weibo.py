# -*- coding: utf-8 -*-
import urllib.request
import json

id='2360812967'
count = 0

proxy_addr="122.241.72.191:808"

def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http':proxy_addr})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data

def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if(data.get('tab_type')=='weibo'):
            containerid=data.get('containerid')
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
    while True:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
         #with open(file,'a',encoding='utf-8') as fh:
            #fh.write(json.dumps(content))

            #print(content)
            cards=content.get('cards')
            if(len(cards)>0):
                
                for j in range(len(cards)):
                    print("-----No"+str(i)+"page,No"+str(j)+"weibo------")
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
                        
                
                i+=1   
            else:
                break
        except Exception as e:
            print(e)
            pass

if __name__=="__main__":
    file=id+".txt"
    #get_userInfo(id)
    get_weibo(id,file)
