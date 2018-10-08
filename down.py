# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 20:00:23 2018

@author: zhangbo
"""

"""
Created on Tue Sep 25 15:01:30 2018

@author: zhangbo
"""

import base64
import os
import requests
import json
os.chdir("C:\\Users\\RenYuan\\PycharmProjects\\Dowloader")

def get_list(url):
    response=requests.get(url)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_pret=soup.prettify()
    td_tags = soup.find_all("div", attrs={"class": "item "})
    item=td_tags[0]
    li=[]
    ti=[]

    for item in td_tags:
        sd=str(item)
        sw=sd.find('href=')
        ew=sd.find('style=\"\" title=')
        www=sd[sw+len('href='):ew]
        www=www.replace('\"','')
        www=www.replace(' ','')
        title_s=sd.find('style=\"\" title=\"')
        title_e=sd.find('\">\n<div class=\"img">')
        title=sd[title_s+len('style=\"\" title=\"'):title_e]
        li.append(www)
        ti.append(title)
    return li,ti
def down_moive(down_url,title):
    response=requests.get(down_url, stream=True, verify=False)
    if response.status_code==200:
        content_size = int(response.headers['content-length'])
        chunk_size = 1024
        if (content_size/chunk_size/1024)<100:
            print('[File Size]: %0.2f MB' % (content_size/chunk_size/1024))
            print('Too small,do not download!')
            return 0
        print('[File Size]: %0.2f MB' % (content_size/chunk_size/1024))
        size = 0
        import sys
        with open(title+'.mp4', 'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)
                f.flush()
                
                print("\r {}".format('[Progress]: %0.2f%%' % float(size/content_size*100) + '\r'),end="")
    
    #            sys.stdout.write('[Progress]: %0.2f%%' % float(size/content_size*100) + '\r')
                sys.stdout.flush()
    print('\n')
    return 1

url="http://www.69tang11.com/"
li,ti=get_list(url)
#data={
#'mode'	:'async',
#'function':	'get_block',
#'block_id':	'list_videos_most_recent_videos',
#'sort_by':	'post_date',
#'from':	5,
#'_':	'1538037519843',
#}



page=2
i=0
while i<len(li):
    url=li[i]
    
    header={'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.69tang11.com',
            'Proxy-Connection': 'Keep-Alive',
            
            }    
    
    response=requests.get(url,headers=header)
    con=str(response.text)
    
    down_s=con.find('video_url: \'')
    down_e=con.find('\', \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tpostfix:')
    down_url=con[down_s+len('video_url: \''):down_e]

    rnd_s=con.find('rand=')
    rnd_e=con.find('\" alt=\"验证码\"')
    rnd=con[rnd_s+len('rand='):rnd_e]
    
    down_url=down_url+'?rnd='+rnd
    print(i,ti[i])
    down_moive(down_url,ti[i])
#    response=requests.get(down_url, stream=True, verify=False)
#    if response.status_code==200:
#        content_size = int(response.headers['content-length'])
#        chunk_size = 1024
#        if (content_size/chunk_size/1024)<100:
#            print('[File Size]: %0.2f MB' % (content_size/chunk_size/1024))
#            print('Too small,do not download!')
#            continue
#        print('[File Size]: %0.2f MB' % (content_size/chunk_size/1024))
#        size = 0
#        title=ti[i]
#        import sys
#        with open(title+'.mp4', 'wb') as f:
#            for data in response.iter_content(chunk_size=chunk_size):
#                f.write(data)
#                size += len(data)
#                f.flush()
#                
#                print("\r {}".format('[Progress]: %0.2f%%' % float(size/content_size*100) + '\r'),end="")
#    
#    #            sys.stdout.write('[Progress]: %0.2f%%' % float(size/content_size*100) + '\r')
#                sys.stdout.flush()
#        print('\n')
    i=i+1
    if i==len(li):
        url='http://www.69tang11.com/?mode=async&function=get_block&block_id=list_videos_most_recent_videos&sort_by=post_date&from='+str(page)+'&_=1538037519843' 
        li,ti=get_list(url)
        i=0
        print('page',page)
        page=page+1
