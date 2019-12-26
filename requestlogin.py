import requests
from lxml import etree


class TwitterLogin(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
        self.login_url = 'https://twitter.com/sessions'
        self.base_url = 'https://twitter.com/login'
        self.logined_url = 'https://twitter.com/home'
        self.session = requests.Session()
    def get_post_data(self):
        post_data={}
        response = self.session.get(self.base_url)
        selector = etree.HTML(response.text)
        # print(response.text)
        authenticity_token = selector.xpath('//form[@data-element="login"]/input[@name="authenticity_token"]/@value')[0]
        # ui_metrics = selector.xpath('//form[@data-element="login"]/input[@name="ui_metrics"]/@value')[0]
        print(authenticity_token)
        post_data['session[username_or_email]'] = '1244192592@qq.com'
        post_data['session[password]'] = '1244192592wang'
        post_data['authenticity_token'] = authenticity_token
        post_data['scribe_log'] = ''
        return post_data

    def login(self, email=None, password=None):
        post_data = {
            'ck': '',  # 可选
            'name': email,
            'password': password,
            'ticket': '',  # 可选

        }
        post_data = self.get_post_data()
        response = self.session.post(self.login_url, data=post_data, headers=self.headers)

        if response.status_code == 200:
            response = self.session.get(self.logined_url)
            import time
            time.sleep(3)
            print(response.text)
            selector = etree.HTML(response.text)
            username = selector.xpath('//img[@alt="王小王小玉"]/@alt')[0]
            print('登录成功:这是%s' % username)
        else:
            print('登录失败:%s' % response.json().get('description'))


if __name__ == "__main__":
    login = TwitterLogin()
    login.login()
    # login.get_post_data()
    # login.login(email='xxx@qq.com', password='xxx')