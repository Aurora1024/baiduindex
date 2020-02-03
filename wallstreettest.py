import time
import datetime
import re
import sys
import logging.config

from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree
from config import logger_path
from xvfbwrapper import Xvfb

def get_news(conn, max_date, current_time):
    """
    华尔街见闻抓取
    :param conn:
    :param max_date: 数据库中最新新闻的日期
    :param current_time: 当前时间
    :return:
    """
    func_name = "采集华尔街见闻"
    logger.debug('start %s ' % func_name)
    spider_data = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    driver = None
    try:
        xvfb = Xvfb(width=1280, height=720)
        xvfb.start()
        driver = webdriver.Chrome(r"/Users/chromedriver")
        #driver = webdriver.Firefox(executable_path=chromedriver_path)
        driver.get('https://wallstreetcn.com/live/global')
        # 让页面滚动到下面,window.scrollBy(0, scrollStep),ScrollStep ：间歇滚动间距
        js = 'window.scrollBy(0,3000)'
        driver.execute_script(js)
        time.sleep(5)
        js = 'window.scrollBy(0,60000)'
        driver.execute_script(js)
        time.sleep(5)
        pages = driver.page_source
        soup = BeautifulSoup(pages, 'html.parser')

        soup1 = soup.find('div', class_='livenews-main')
        content = soup1.find_all('div', class_='live-item')
        news_source = '华尔街见闻'
        news_type = '宏观'
        last_news_time = '23:59'
        d_date = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        for cont in content:
            news_time = cont.find('time', attrs={'class': 'live-item_created'}).get_text()
            news = cont.find('div', attrs={'class': 'live-item_main'}).find('div', attrs={'class': 'live-item_html'})
            if news is None:
                return
            news = news.get_text().strip().replace('//', '')
            if last_news_time < news_time:
                d_date = d_date - datetime.timedelta(days=1)
            s_date = d_date.strftime("%Y-%m-%d")
            over_time = s_date + ' ' + news_time
            print(over_time)
            if max_date > over_time:
                break
            # sql_params = [over_time, spider_data, news_source, news_type, news]
            # logger.debug(sql_cj)
            # logger.debug(sql_params)
            # execute_sql(conn, sql_cj, sql_params)
            df = pd.DataFrame([temp], columns=['over_time', 'spider_data', 'news_source', 'news_type', 'news'])
            res= res.append(df,ignore_index=True)
            last_news_time = news_time
        logger.debug('end %s ' % func_name)
    except Exception as e:
        msg = func_name + ' 处理失败: ' + str(e)
        logger.error(msg)
    finally:
        if driver:
            # driver.close()
            driver.quit()
            xvfb.stop()


def save_file(data):
    n = datetime.datetime.now()
    s_date = n.strftime("%Y%m%d")
    save_path = html_path + s_date + '_sina.txt'
    f_obj = open(save_path, 'wb')  # wb 表示打开方式,也可用w
    f_obj.write(data)
    f_obj.close()


def main():
    now = datetime.datetime.now()
    conn = None
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    res = pd.DataFrame(columns=['over_time', 'spider_data', 'news_source', 'news_type', 'news'])
    max_date_news = 0
    get_news(conn, max_date_news, current_time)
    res.to_csv("result"+current_time+".csv", sep=',')


if __name__ == '__main__':
    main()