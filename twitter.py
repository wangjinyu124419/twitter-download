import os
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# import gevent
# from gevent import monkey
# monkey.patch_all()
import requests
from lxml import etree
import re
from twitter_video_downloader.twitter_dl import  TwitterDownloader

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
url='https://twitter.com/SLAMKicks/status/1207786564602015745'
# file='SLAMKicks.txt'
file=r'D:\pycharm project\twitter_media\follow\Ding1204.txt'
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080',
}
user='Ding1204'
def count_time(fun):
    def warpper(*args):
        s_time=time.time()
        fun(*args)
        e_time=time.time()
        t_time=e_time-s_time
        print('%s耗时：%s'%(fun.__name__,t_time))
    return warpper

def get_twitter(file):
    pic_t_list=[]
    with open(file,encoding='utf8') as f:
        t_list=f.readlines()
        for twitter in t_list:
            res=re.match('.*(pic.twitter.com.*)',twitter)
            if res:
                pic_t_list.append(res.group(1))
    pic_t_list = ['https://'+ pic_t for pic_t in pic_t_list]
    print(pic_t_list)
    return pic_t_list

def get_pics_url(url):
    page_source=requests.get(url,timeout=10,proxies=proxies).content
    selector = etree.HTML(page_source)
    # print('url:%s,page_source:%s'%(url,page_source))
    # pic_urls=selector.xpath('//div[@class="AdaptiveMedia-quadPhoto"]//img/@src')
    pic_urls=selector.xpath('//div[@class="permalink-inner permalink-tweet-container"]//img[starts-with(@src,"https://pbs.twimg.com/media")]/@src')
        # pic_urls=selector.xpath('//div[@class="AdaptiveMedia-quadPhoto"]//img/@src')
    # print('pic_urls:%s'%pic_urls)
    # is_video=selector.xpath('//video[@preload="none"]/@src')


    return pic_urls

def downloadpic(url,path):
    name=url.split('/')[-1]
    file_path=os.path.join(path,name)
    if os.path.exists(file_path):
        print('已下载:%s'%file_path)
    pic_content=requests.get(url,timeout=10,proxies=proxies).content
    with open(file_path,'wb') as f:
        f.write(pic_content)
        print(file_path)

def download(pic_t,path):
    print('download:%s'%pic_t)
    pic_urls = get_pics_url(pic_t)
    for pic_url in pic_urls:
        downloadpic(pic_url,path)

    if not pic_urls:
        res=requests.get(pic_t,proxies=proxies)
        print(res.url)
        twitter_dl = TwitterDownloader(res.url,output_dir=path)
        twitter_dl.download()




def count_pic():
    l=os.listdir('download_twitter')
    print('图片数量:%d'%len(l))
@count_time
def main():
    path=os.path.join('download_twitter',user)
    pic_t_list = get_twitter(file)
    print('pic_t_list:%s'%len(pic_t_list))
    # g_list=[]
    t_list=[]
    with ThreadPoolExecutor() as executor:
        for pic_t in pic_t_list:
            obj = executor.submit(download, pic_t,path)
            t_list.append(obj)
        as_completed(t_list)

    # download(pic_t)
        # g_list.append(gevent.spawn(download,pic_t))
    # gevent.joinall(g_list)
    count_pic()




if __name__ == '__main__':

    main()





