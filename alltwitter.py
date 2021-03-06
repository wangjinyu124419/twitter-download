import os
import sys
import locale
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from retry import retry

from twint import twint


# from twitter import count_time


# Configure
class AllTwitter():
    def __init__(self, user=''):
        self.user = user
        self.following_file = self.user + '.txt'
        self.save_dir = 'follow'

    def get_all_followling(self):
        c = twint.Config()
        c.Username = self.user
        c.Proxy_host = '127.0.0.1'
        c.Proxy_port = '1080'
        c.Proxy_type = 'http'
        c.Following = True
        c.Output = self.following_file
        # self.following_file=c.Output
        twint.run.Following(c)
        self.resort()

    def resort(self):
        with open(self.following_file, encoding='utf8') as f:
            following_list = f.readlines()
            following_list.sort()
        with open(self.following_file, 'w', encoding='utf8') as f:
            f.writelines(following_list)

    # @retry(delay=10, tries=5, backoff=2, max_delay=160)
    def get_one_user(self, follow):
        c = twint.Config()
        c.Proxy_host = '127.0.0.1'
        c.Proxy_port = '1080'
        c.Proxy_type = 'http'
        c.Username = follow
        # c.Profile_full = True
        c.Output = os.path.join(self.save_dir, follow + '.txt')
        # c.Media = True
        # c.Videos = True
        # c.Since = '2019-12-20'
        # c.Until = '2020-01-08'
        twint.run.Search(c)
        # twint.run.Profile(c)
        print('%s已完成' % follow)
        with open('finish.txt', 'a') as f:
            f.write(follow + '\n')

    # @count_time
    def get_all_twitter(self):
        with open(self.following_file, encoding='utf8') as f:
            follow_list = [follow.strip() for follow in f.readlines()]
            with ProcessPoolExecutor(max_workers=1) as executor:
                t_dict = {executor.submit(self.get_one_user, follow): follow for follow in follow_list}
                for future in as_completed(t_dict):
                    follow = t_dict[future]
                    try:
                        future.result()
                    except Exception:
                        print('get_one_user异常:%s' % follow + '\n', traceback.format_exc())

    def get_pic_url(self):
        pass

    def main(self):
        self.get_all_followling()
        self.get_all_twitter()


if __name__ == '__main__':
    at = AllTwitter('miss')
    # at.get_all_twitter()
    # at.get_all_followling()
    at.get_one_user('dongxiaoniu')
    # at.main()
