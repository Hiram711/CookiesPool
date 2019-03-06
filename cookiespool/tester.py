import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class RmHnairValidTester(ValidTester):
    def __init__(self, website='rmhnair'):
        ValidTester.__init__(self, website)
        self.test_url = 'http://rm.hnair.com/ajax/Yeesky.EIM.Site.BI.ClassTune.AjaxClass.FlightTuneAjax,Yeesky.EIM.Site.BI.ClassTune.ashx?_method=GetLimitedCompany&_session=r'
        self.headers = {'Host': 'rm.hnair.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
                        'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'http://rm.hnair.com/BI/ClassTune/WebUI/FlightTune.aspx',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Connection': 'keep-alive',
                        }

    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            response = requests.post(self.test_url, cookies=cookies, timeout=5, allow_redirects=False,
                                     headers=self.headers)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)


if __name__ == '__main__':
    RmHnairValidTester().run()
