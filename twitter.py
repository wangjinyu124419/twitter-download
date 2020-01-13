import multiprocessing
import os
import threading
import time
import re
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures import as_completed
from you_get.extractors.twitter import twitter_download

import requests
from lxml import etree
from retry import retry

from twitter_video_downloader.twitter_dl import TwitterDownloader
from alltwitter import AllTwitter

lock = multiprocessing.Lock()
base_dir = r'K:\爬虫\twitter\download_twitter'
pre_url = 'https://twitter.com/'


def count_time(fun):
    def warpper(*args):
        s_time = time.time()
        arg = args[1] if len(args) > 1 else '-'
        fun(*args)
        e_time = time.time()
        t_time = e_time - s_time
        print('%s耗时：%s,参数:%s' % (fun.__name__, t_time, arg))

    return warpper


class Twitter():
    def __init__(self):
        self.proxies = {
            'http': 'http://127.0.0.1:1080',
            'https': 'https://127.0.0.1:1080',
        }
        # self.follow_dir = 'memberlist'
        self.follow_dir = 'follow'
        self.recorder_file = 'recorder_file.txt'
        with open(self.recorder_file) as f:
            self.recoder_list = [url.strip() for url in f.readlines()]
        if not os.path.exists(self.recorder_file):
            with open(self.recorder_file, 'w') as f:
                pass
        # self.w_file=open(self.recorder_file,'w')
        # self.r_file=open(self.recorder_file,'r')

    # @retry(delay=10, tries=5, backoff=2, max_delay=160)
    def get_nickname(self, follow):
        url = pre_url + follow
        try:
            page_source = requests.get(url, timeout=30, proxies=self.proxies).text
            selector = etree.HTML(page_source)
            nickname = selector.xpath('//h1[@class="ProfileHeaderCard-name"]/a/text()')[0]
        except:
            nickname = follow
        legal_nickname = re.sub(r"[\/\\\:\*\?\"\<\>\|!！\.\s]", "", nickname)
        return legal_nickname

    def get_twitter(self, file):
        pic_t_list = []
        with open(file, encoding='utf8') as f:
            t_list = f.readlines()
            for twitter in t_list:
                res = re.match('.*(pic.twitter.com/\w*)', twitter)
                if res:
                    pic_t_list.append(res.group(1))
        pic_t_list = ['https://' + pic_t for pic_t in pic_t_list]
        # print(pic_t_list)
        return pic_t_list

    # @retry(delay=10, backoff=2, max_delay=160)
    def get_pics_url(self, url):
        page_source = requests.get(url, timeout=30, proxies=self.proxies).text
        selector = etree.HTML(page_source)
        # print('url:%s,page_source:%s'%(url,page_source))
        # pic_urls=selector.xpath('//div[@class="AdaptiveMedia-quadPhoto"]//img/@src')
        # pic_urls = selector.xpath(
        # '//div[@class="permalink-inner permalink-tweet-container"]//img[starts-with(@src,"https://pbs.twimg.com/media")]/@src')
        # if not pic_urls:
        pic_urls = selector.xpath('//meta[starts-with(@content,"https://pbs.twimg.com/media")]/@content')

        gif_urls = selector.xpath('//meta[starts-with(@content,"https://pbs.twimg.com/tweet_video_thumb")]/@content')

        # print('url:%s\npic_urls:%s'%(url,pic_urls))
        return pic_urls, gif_urls

    # @retry(delay=10, backoff=2, max_delay=160)
    def downloadpic(self, url, path):
        name = url.split('/')[-1].split(":")[0]
        file_path = os.path.join(path, name)
        if os.path.exists(file_path):
            print('文件已存在:%s' % file_path)
            return
        pic_content = requests.get(url, timeout=30, proxies=self.proxies).content
        with open(file_path, 'wb') as f:
            f.write(pic_content)
            print(file_path)

    # @retry(delay=10, backoff=2, max_delay=160)
    def downloadgif(self, url, path):
        # https://pbs.twimg.com/tweet_video_thumb/Du3_VqvVsAAjB41.jpg
        # https://video.twimg.com/tweet_video/Du3_VqvVsAAjB41.mp4
        base_gif_url = 'https://video.twimg.com/tweet_video/{}.mp4'
        name = url.split('/')[-1].split(".")[0]
        gif_url = base_gif_url.format(name)
        file_path = os.path.join(path, name + '.mp4')
        if os.path.exists(file_path):
            print('文件已存在:%s' % file_path)
            return
        pic_content = requests.get(gif_url, timeout=30, proxies=self.proxies).content
        with open(file_path, 'wb') as f:
            f.write(pic_content)
            print(file_path)

    def count_pic(self, path):
        l = os.listdir(path)
        print('下载数量:%d' % len(l))

    def check_repeat(self, url):
        try:
            if url in self.recoder_list:
                print('已经下载:%s' % url)
                return True
            # with open(self.recorder_file) as f:
            #     url_list = [ url.strip() for url in f.readlines()]
            #     if url in url_list:
            #         print('已经下载:%s'%url)
            #         return True
        except Exception:
            print(traceback.format_exc())

    def record_repeat(self, url):
        with open(self.recorder_file, 'a') as f:
            f.write(url + '\n')

    # @count_time
    # @retry(delay=10, tries=5, backoff=2, max_delay=160)
    def download(self, pic_t, path):
        status_code = requests.get(pic_t, proxies=self.proxies, timeout=30).status_code
        if status_code != 200:
            print('%s状态码错误:%d' % (pic_t, status_code))
            self.record_repeat(pic_t)
            return
        real_url = requests.get(pic_t, proxies=self.proxies, timeout=30).url
        if 'status' not in real_url:
            print("地址异常:%s" % real_url)
            return
        print("当前执行的线程为:%s,url:%s" % (threading.current_thread(), real_url))
        pic_urls, gif_urls = self.get_pics_url(real_url)
        if pic_urls:
            for pic_url in pic_urls:
                self.downloadpic(pic_url, path)
        if gif_urls:
            for pic_url in gif_urls:
                self.downloadgif(pic_url, path)
        if not pic_urls and not gif_urls:
            try:
                twitter_download(real_url, output_dir=path)
            except Exception as e:
                print('twitter_download异常:%s' % pic_t, e)
                try:
                    twitter_dl = TwitterDownloader(real_url, output_dir=path)
                    lock.acquire()
                    print("上锁:%s" % real_url)
                    twitter_dl.download()
                finally:
                    lock.release()
                    print("解锁:%s" % real_url)
        self.record_repeat(pic_t)

    def thread_download(self,path,pic_t_list):
        # thead pool
        with ThreadPoolExecutor() as executor:
            t_dict = {executor.submit(self.download, pic_t, path): pic_t for pic_t in pic_t_list if
                      not self.check_repeat(pic_t)}
            for future in as_completed(t_dict):
                url = t_dict[future]
                try:
                    future.result()
                except Exception:
                    print('download异常:%s' % url + '\n', traceback.format_exc())

            # process pool
            # p_list = []
            # with ProcessPoolExecutor() as executor:
            #     for pic_t in pic_t_list:
            #         if self.check_repeat(pic_t):
            #             continue
            #         obj = executor.submit(self.download, pic_t, path)
            #         p_list.append(obj)
            #     for future in as_completed(p_list):
            #         try:
            #             future.result()
            #         except Exception:
            #             print('pic_t:%s'%pic_t+'\n', traceback.format_exc())
            # single thread
            # for pic_t in pic_t_list:
            #     self.download(pic_t,path)

    def download_one(self,user=None):
        at = AllTwitter()
        at.get_one_user(user)
        nick_name = self.get_nickname(user)
        path = os.path.join(base_dir, nick_name)
        if not os.path.exists(path):
            os.makedirs(path)
            print('创建：%s' % nick_name)
        pic_t_list = self.get_twitter(os.path.join(self.follow_dir, user+'.txt'))
        self.thread_download(path,pic_t_list)
        self.count_pic(path)
    @count_time
    def main(self):
        at = AllTwitter(user='memberlist')
        # at.main()
        # at.get_all_twitter()
        at.get_one_user('feitunmugou091')
        follow_list = os.listdir(self.follow_dir)
        for follow in follow_list:
            print('download user:%s' % follow)
            nick_name = self.get_nickname(follow.split('.')[0])
            path = os.path.join(base_dir, nick_name)
            if not os.path.exists(path):
                os.makedirs(path)
                print('创建：%s' % nick_name)
            pic_t_list = self.get_twitter(os.path.join(self.follow_dir, follow))
            # pic_t_list = ['https://pic.twitter.com/LYvQA7I5Dn','123']
            print('pic_t_list:%s' % len(pic_t_list))
            self.thread_download(path,pic_t_list)
            self.count_pic(path)


if __name__ == '__main__':
    t = Twitter()
    t.download_one('yaojing2019')
    # t.main()
