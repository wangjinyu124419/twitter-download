import os
import sys
import locale
from twint import twint



# Configure
class AllTwitter():
    def __init__(self, user,):
        self.user = user
        self.following_file = user+'.txt'
        self.save_dir='follow'

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
            following_list=f.readlines()
            following_list.sort()
        with open(self.following_file, 'w', encoding='utf8') as f:
            f.writelines(following_list)

    def get_all_twitter(self):
        with open(self.following_file, encoding='utf8') as f:
            follow_list = [follow.strip() for follow in f.readlines()]
            for follow in follow_list:
                c = twint.Config()
                c.Proxy_host = '127.0.0.1'
                c.Proxy_port = '1080'
                c.Proxy_type = 'http'
                c.Username = follow
                c.Output = os.path.join(self.save_dir, follow + '.txt')
                # c.Media = True
                # c.Videos = True
                # c.Since = '2019-12-01'
                twint.run.Search(c)

    def get_pic_url(self):
        pass

    def main(self):
        self.get_all_followling()
        self.get_all_twitter()


if __name__ == '__main__':
    at = AllTwitter('jordan124419')
    at.get_all_twitter()
    # at.get_all_followling()
    # at.resort()