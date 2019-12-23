from nineporn import *


class Peta(NinePorn):
    def __init__(self):
        super().__init__()
        self.root_dir = r'K:\爬虫\twitter'
        self.login_url = 'https://twitter.com/login'
        self.finish_file = 'twitter.txt'
    def login(self):
        self.driver.get(self.login_url)
        username = self.driver.find_element_by_xpath('//div[@class="page-canvas"]//input[@name="session[username_or_email]"]')
        password = self.driver.find_element_by_xpath('//div[@class="page-canvas"]//input[@name="session[password]"]')
        enter = self.driver.find_element_by_xpath('//button[@type="submit"]')
        username.send_keys('Jordan124419')
        password.send_keys('1244192592wang')
        enter.click()

    @count_time
    def get_pic_list(self, detail_url):
        try:
            self.driver.get(detail_url)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            wait = WebDriverWait(self.driver, self.pic_list_time)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="图像"]/img')))
            page_source = self.driver.page_source
            selector = etree.HTML(page_source)
            small_url_list = selector.xpath('//div[@aria-label="图像"]/img/@src')
            pic_url_list=[url.split('&')[0] for url in small_url_list]
            print("pic_url_list:%s, url:%s" % (len(pic_url_list), detail_url))
            return pic_url_list
        except Exception:
            print('get_pic_list失败：%s' % detail_url)
            print(traceback.format_exc())
            return []


    def check_repeat_url(self, url):
        try:
            # unique_key=url.split("/")[-1]
            unique_key = re.match('.*(\d{7}).*', url).group(1)
            with open(self.finish_file, 'r', encoding='utf8') as f:
                content_list = f.readlines()
                for content in content_list:
                    if unique_key in content:
                        print('已经下载过：%s' % (content.strip()))
                        return True
        except Exception:
            print(traceback.format_exc())

    @count_time
    def download(self, detail_url):
        pic_list = self.get_pic_list(detail_url)
        if not pic_list:
            print('pic_list为空:%s'%(detail_url))
            return
        print('开始下载:%s' % detail_url)
        g_list = []
        for pic_url in pic_list:
            g_list.append(gevent.spawn(self.save_pic, pic_url))
        gevent.joinall(g_list)

    # @count_time
    def save_pic(self,url):
        try:
            name = url.split('media/')[1].split('?')[0]+'.jpg'
        except Exception as e:
            print(e,url)
            return
        pic_path = os.path.join(self.root_dir, name)
        if os.path.exists(pic_path):
            print('文件已存在:%s' % pic_path)
            return
        for i in range(5):
            try:
                status_code = requests.get(url,timeout=10).status_code
                if status_code != 200:
                    print("status_code:%s" % status_code)
                    return
                content = requests.get(url,timeout=20).content
                with open(pic_path, 'wb') as f:
                    f.write(content)
                    print(pic_path)
                    return
            except Exception as e:
                print('保存失败第%d次，url:%s,异常信息:%s'%(i+1,url,e))
                time.sleep(i)
                continue
        else:
            print(traceback.format_exc())
            print('save_pic失败：%s' % url)

    def get_twitter(self,file):
        url_list = []
        with open(file, encoding='utf8') as f:
            files = f.readlines()
            for file in files:
                res = re.match('.*(pic.twitter.com.*)', file)
                if res:
                    url_list.append(res.group(1))

        full_url_list= ['https://'+url for url in url_list]
        return full_url_list
    @count_time
    def main(self):
        self.login()
        url_list =self.get_twitter('file.txt')
        for url  in url_list:

            self.download(url)


if __name__ == '__main__':
    peta = Peta()
    peta.main()
