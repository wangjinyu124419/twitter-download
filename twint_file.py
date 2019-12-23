import os

from twint import twint

# Configure
class AllTwitter():
    following_file='Ding1204.txt'
    def get_all_followling(self):
        c = twint.Config()
        c.Username = "jordan124419"
        c.Proxy_host = '127.0.0.1'
        c.Proxy_port = '1080'
        c.Proxy_type = 'http'
        c.Following = True
        c.Output = 'Ding1204.txt'
        self.following_file=c.Output
        twint.run.Following(c)
    def get_all_twitter(self):

        with open(self.following_file,encoding='utf8') as f:
            follow_list = [follow.strip() for follow in f.readlines()]
            for follow in follow_list:
                c = twint.Config()
                c.Proxy_host = '127.0.0.1'
                c.Proxy_port = '1080'
                c.Proxy_type = 'http'
                c.Username = follow
                c.Output = os.path.join('follow',follow+'.txt')
                c.Media = True
                twint.run.Search(c)
        # twint.run.Search(c)


    def get_pic_url(self):
        pass

    def main(self):
        self.get_all_followling()
        self.get_all_twitter()

if __name__ == '__main__':
    at=AllTwitter()
    at.get_all_twitter()

