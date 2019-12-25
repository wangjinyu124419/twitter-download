import os
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import requests
from lxml import etree
import re
from twitter_video_downloader.twitter_dl import TwitterDownloader

def count_time(fun):
    def warpper(*args):
        s_time = time.time()
        fun(*args)
        e_time = time.time()
        t_time = e_time - s_time
        print('%s耗时：%s' % (fun.__name__, t_time))
    return warpper


class Twitter():
    def __init__(self):
        self.proxies = {
            'http': 'http://127.0.0.1:1080',
            'https': 'https://127.0.0.1:1080',
        }
        self.orgin_file = r'124419.txt'
        self.user = 'Ding1204'
        self.follow_dir='follow'

    def get_twitter(self, file):
        pic_t_list = []
        with open(file, encoding='utf8') as f:
            t_list = f.readlines()
            for twitter in t_list:
                res = re.match('.*(pic.twitter.com.*)', twitter)
                if res:
                    pic_t_list.append(res.group(1))
        pic_t_list = ['https://' + pic_t for pic_t in pic_t_list]
        # print(pic_t_list)
        return pic_t_list

    def get_pics_url(self, url):
        page_source = requests.get(url, timeout=10, proxies=self.proxies).text
        selector = etree.HTML(page_source)
        # print('url:%s,page_source:%s'%(url,page_source))
        # pic_urls=selector.xpath('//div[@class="AdaptiveMedia-quadPhoto"]//img/@src')
        # pic_urls = selector.xpath(
            # '//div[@class="permalink-inner permalink-tweet-container"]//img[starts-with(@src,"https://pbs.twimg.com/media")]/@src')
        # if not pic_urls:
        pic_urls=selector.xpath('//meta[starts-with(@content,"https://pbs.twimg.com/media")]/@content')

        #gif
        if not pic_urls:
            pic_urls = selector.xpath('//meta[starts-with(@content,"https://pbs.twimg.com/tweet_video_thumb")]/@content')

            # print('url:%s\npic_urls:%s'%(url,pic_urls))
        return pic_urls

    def downloadpic(self, url, path):
        name = url.split('/')[-1].split(":")[0]
        file_path = os.path.join(path, name)
        if os.path.exists(file_path):
            print('已下载:%s' % file_path)
            return
        pic_content = requests.get(url, timeout=10, proxies=self.proxies).content
        with open(file_path, 'wb') as f:
            f.write(pic_content)
            print(file_path)
    def downloadgif(self, url, path):
        #https://pbs.twimg.com/tweet_video_thumb/Du3_VqvVsAAjB41.jpg
        #https://video.twimg.com/tweet_video/Du3_VqvVsAAjB41.mp4
        base_gif_url='https://video.twimg.com/tweet_video/{}.mp4'
        name = url.split('/')[-1].split(".")[0]
        gif_url = base_gif_url.format(name)
        file_path = os.path.join(path, name+'.mp4')
        if os.path.exists(file_path):
            print('已下载:%s' % file_path)
            return
        pic_content = requests.get(gif_url, timeout=30, proxies=self.proxies).content
        with open(file_path, 'wb') as f:
            f.write(pic_content)
            print(file_path)


    def download(self, pic_t, path):
        real_url = requests.get(pic_t, proxies=self.proxies).url
        if 'video' in real_url:

            twitter_dl = TwitterDownloader(real_url, output_dir=path)
            twitter_dl.download()

        else:
            pic_urls = self.get_pics_url(real_url)
            if not pic_urls:
                print('pic_urls:%s'%real_url)

            for pic_url in pic_urls:
                if 'tweet_video_thumb' in pic_url:
                    self.downloadgif(pic_url,path)
                    continue
                self.downloadpic(pic_url, path)



    def count_pic(self,path):
        l = os.listdir(path)
        print('图片数量:%d' % len(l))

    @count_time
    def main(self):
        follow_list = os.listdir(self.follow_dir)
        for follow in follow_list:
            print('download user:%s'%follow)
            path = os.path.join('download_twitter', follow.split('.')[0])
            if not os.path.exists(path):
                os.makedirs(path)
            pic_t_list = self.get_twitter(os.path.join(self.follow_dir, follow))
            print('pic_t_list:%s' % len(pic_t_list))


            # thead pool
            t_list = []
            # with ThreadPoolExecutor(max_workers=8) as executor:
            with ThreadPoolExecutor() as executor:
                for pic_t in pic_t_list:
                    obj = executor.submit(self.download, pic_t, path)
                    t_list.append(obj)
                for future in as_completed(t_list):
                    try:
                        future.result()
                    except Exception as e:
                        print(pic_t,e)

                as_completed(t_list)



            # single thread
            # for pic_t in pic_t_list:
            #     self.download(pic_t,path)


            self.count_pic(path)


if __name__ == '__main__':
    t = Twitter()
    t.main()
