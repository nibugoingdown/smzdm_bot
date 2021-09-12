"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            #print(result)
            print("什么值得买连续签到天数：%s" % (result['data']['checkin_num']))
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    # print(res)
    print("什么值得买连续签到天数：%s" % (res['data']['checkin_num']))
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = "值得买已签到%s天" % (res['data']['checkin_num']),
                        # desp = str(res),
                        desp = "本周连续签到天数：%s" % (res['data']['continue_checkin_days']),
                        secretKey = SERVERCHAN_SECRETKEY)
        
    sb1 = SMZDM_Bot()
    cookies = os.environ["COOKIES1"]
    sb1.load_cookie_str(cookies)
    res1 = sb1.checkin()
    print("什么值得买连续签到天数：%s" % (res1['data']['checkin_num']))
    SERVERCHAN_SECRETKEY = os.environ["SERVERCHAN_SECRETKEY1"]
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = "值得买已签到%s天" % (res1['data']['checkin_num']),
                        # desp = str(res1),
                        desp = "本周连续签到天数：%s" % (res1['data']['continue_checkin_days']),
                        secretKey = SERVERCHAN_SECRETKEY)
    print('代码完毕')
