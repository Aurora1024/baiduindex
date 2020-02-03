from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import random,string,os,time,json

def gen_random_string(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))
    # return ''.join(random.sample(string.ascii_letters, slen))


def get_cookie_from_network(account,password,cookies_dir='cookies'):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(r"/Users/chromedriver")
    driver.get('https://index.baidu.com/#/')
    time.sleep(3)
    driver.find_element_by_class_name("username-text").click()
    time.sleep(3)
    driver.find_element_by_id("TANGRAM__PSP_4__userName").send_keys(account)
    driver.find_element_by_id("TANGRAM__PSP_4__password").send_keys(password)


    if not os.path.exists(cookies_dir):
        os.makedirs(cookies_dir)
    cookies_list = [f for f in os.listdir(cookies_dir)]
    while True:
        cookies_name = '%s.cookie' % gen_random_string(10)
        if cookies_name not in cookies_list:
            cookies_path = os.path.join(cookies_dir, cookies_name)
            break
    #json.dump(driver.get_cookies(), open(cookies_path, 'w'))
    while 1:
        jud2 = input("登录好后输入1：")
        if jud2 == '1':
            # pickle.dump(browser.get_cookies(), open("cookies.pkl", 'wb'))
            json.dump(driver.get_cookies(), open(cookies_path, 'w'))
            break

    # cookie_list = driver.get_cookies()
    # print(cookie_list)
    #
    # cookie_dict = {}
    # for cookie in cookie_list:
    #     #写入文件
    #     f = open(cookie['name']+'.cookie','w')
    #     #pickle.dump(cookie, f)
    #     json.dump(cookie, f)
    #     f.close()
    #
    #     if cookie.has_key('name') and cookie.has_key('value'):
    #         cookie_dict[cookie['name']] = cookie['value']

    # driver.get('https://www.baidu.com')
    # driver.delete_all_cookies()
    #
    # if not os.path.exists(cookies_dir):
    #     os.makedirs(cookies_dir)
    # cookies_list = [f for f in os.listdir(cookies_dir)]
    # while True:
    #     cookies_name = '%s.cookie' % gen_random_string(10)
    #     if cookies_name not in cookies_list:
    #         cookies_path = os.path.join(cookies_dir, cookies_name)
    #         break
    # time.sleep(3)
    # driver.find_element_by_class_name("tj_login").click()
    # time.sleep(3)
    # driver.find_element_by_class_name("TANGRAM__PSP_10__footerULoginBtn").click()
    # time.sleep(3)
    # driver.find_element_by_id("TANGRAM__PSP_10__userName").send_keys(account)
    # driver.find_element_by_id("TANGRAM__PSP_10__password").send_keys(password)
    # driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
    # time.sleep(3)
    # driver.get('https://index.baidu.com/#/')
    # time.sleep(.5)
    # json.dump(driver.get_cookies(), open(cookies_path, 'w'))
    # while 1:
    #     break
        # jud2 = input("登录好后输入1(放弃输入0)：")
        # if jud2 == '1':
        #     # pickle.dump(browser.get_cookies(), open("cookies.pkl", 'wb'))
        #     browser.get('https://index.baidu.com/#/')
        #     time.sleep(.5)
        #     json.dump(browser.get_cookies(), open(cookies_path, 'w'))
        #     break
        # elif jud2 == '0':
        #     break
    # cookies = json.load(open(cookies_path, "r"))
    # for cookie in cookies:  # 利用cookies进行登录
    #     browser.add_cookie(cookie)
    # browser.refresh()
    driver.quit()

    #return cookie_dict

# def get_cookie_from_cache():
#
#     cookie_dict = {}
#     for parent, dirnames, filenames in os.walk('./'):
#         for filename in filenames:
#             if filename.endswith('.cookie'):
#                 print filename
#                 with open(self.dir_temp + filename, 'r') as f:
#                     d = json.load(f)
#
#                     if d.has_key('name') and d.has_key('value') and d.has_key('expiry'):
#                         expiry_date = int(d['expiry'])
#                         if expiry_date > (int)(time.time()):
#                             cookie_dict[d['name']] = d['value']
#                         else:
#                             return {}
#
#     return cookie_dict
#
#
# def get_cookie():
#     cookie_dict = get_cookie_from_cache()
#     if not cookie_dict:
#         cookie_dict = get_cookie_from_network()
#
#     return cookie_dict

if __name__ == '__main__':

    # 收集cookies
    df = pd.read_csv('5.csv')
    print(df)
    for index in df.index:
        #account = df.loc[i].values[0]
        #print(df.loc[index].values[0])
        get_cookie_from_network(df.loc[index].values[0], df.loc[index].values[1],cookies_dir="/Users/wukefei/Downloads/wukefei/cookies")

