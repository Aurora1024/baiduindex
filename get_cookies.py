import requests
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import random,string,os,time,json


def gen_random_string(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


def get_cookie_from_network(account,password,email,emailpwd,cookies_dir='cookies'):
    # account='sxk59a3c3n@163.com';password='wt253672';cookies_dir='cookies'
    chrome_options = webdriver.ChromeOptions()
    # url = "https://proxy.horocn.com/api/proxies?order_id=UDGE1616574058408501&num=1&format=json&line_separator=win"
    # p_json = requests.get(url).json()
    # proxy = ['{host}:{port}'.format(**dic) for dic in p_json][0]
    # chrome_options.add_argument('--proxy-server=http://%s' % proxy)
    browser = webdriver.Chrome(r"/Users/chromedriver")
    browser.maximize_window()

    # 百度指数页面
    try:
        browser.get('https://index.baidu.com/#/')
        browser.find_element_by_class_name("username-text").click()
        time.sleep(random.random()+.5)
        browser.find_element_by_id("TANGRAM__PSP_4__userName").send_keys(account)
        time.sleep(random.random()+.5)
        browser.find_element_by_id("TANGRAM__PSP_4__password").send_keys(password)
        browser.find_element_by_id("TANGRAM__PSP_4__submit").click()
        time.sleep(random.random()+.5)
        browser.find_element_by_id("TANGRAM__46__button_send_email").click()
    except:
        print('账号:', account, '密码', password)
        input("收到完成百度页后按任意键继续")

    try:
        # 163邮箱页面
        js='window.open("http://mail.163.com/");'
        browser.execute_script(js)
        handles = browser.window_handles
        
        #切换到表单
        browser.switch_to_window(handles[1])
        time.sleep(random.random()+.5)
        browser.switch_to.frame(browser.find_element_by_xpath("//iframe[contains(@id,'x-URS-iframe')]"))
        time.sleep(random.random())
        browser.find_element_by_name("email").clear()
        time.sleep(random.random())
        browser.find_element_by_name("email").send_keys(email)
        time.sleep(random.random())
        browser.find_element_by_name("password").clear()
        time.sleep(random.random())
        browser.find_element_by_name("password").send_keys(emailpwd)
        time.sleep(random.random())
        browser.find_element_by_id("dologin").click()
    except:
        print('账号:', email, '密码', emailpwd)
        input("收到完成邮箱页后按任意键继续")

    if not os.path.exists(cookies_dir):
        os.makedirs(cookies_dir)
    cookies_list = [f for f in os.listdir(cookies_dir)]

    while True:
        cookies_name = '%s.cookie' % gen_random_string(10)
        if cookies_name not in cookies_list:
            cookies_path = os.path.join(cookies_dir, cookies_name)
            break

    while 1:
        jud2 = input("登录好后输入1(跳过输入0)：")
        if jud2 == '1': 
            # 转入百度窗口
            try:
                browser.switch_to_window(handles[0])
            except:
                pass
            json.dump(browser.get_cookies(), open(cookies_path, 'w'))
            break
        elif jud2 == '0':
            break

    # time.sleep(3)
    browser.quit()


if __name__ == '__main__':

    # 工作文件夹
    #os.chdir("D:/baiduindex_crawler")

    # 收集cookies
    df = pd.read_csv("百度账号5.csv")

    for i, (account,password,email,emailpwd) in df.iterrows():
        get_cookie_from_network(account,password,email,emailpwd,cookies_dir="/Users/wukefei/Downloads/wukefei/cookies")

