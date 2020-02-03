"提取百度指数"

from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import datetime
import time
import pickle
import pandas as pd


def init_browser():
    """
        initialize browser
    """
    global browser
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome('chromedriver')
    prefs = {'profile.managed_default_content_settings.images':2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser.get('https://index.baidu.com/#/')
    browser.set_window_size(1500, 900)
    browser.delete_all_cookies()
    # jud = input('第一次登陆？y/n：')
    jud = 'n'
    if jud == 'y':
        jud2 = input("登录好后输入1：")
        while 1:
            if jud2 == '1':
                break
        pickle.dump(browser.get_cookies(), open("cookies.pkl", 'wb'))
    else:
        cookies = pickle.load(open("cookies.pkl", "rb"))  # 读取之前登录的cookies
        for cookie in cookies:  # 利用cookies进行登录
            browser.add_cookie(cookie)
        browser.refresh()


def get_into_page(keyword):
    """
        get baiduIndex page
    """
    url = 'https://index.baidu.com/v2/main/index.html#/trend?words=%s' % quote(keyword)
    # print(url)
    while True:
        browser.get(url)
        if '频繁' in browser.page_source:
            time.sleep(30)
        else:
            break
    if '未被收录' in browser.page_source:
        return 1
    else:
        return 0


def adjust_time_range(startdate, enddate):
    """
        ...
    """
    time.sleep(2)
    browser.find_element_by_xpath('//*[@class="index-date-range-picker"]').click()
    base_node = browser.find_element_by_xpath('//*[contains(@class, "index-date-range-picker-overlay-box tether-element")]')
    select_date(base_node, startdate)
    end_date_button = base_node.find_elements_by_xpath('.//*[@class="date-panel-wrapper"]')[1]
    end_date_button.click()
    select_date(base_node, enddate)

    base_node.find_element_by_xpath('.//*[@class="primary"]').click()


def select_date(base_node, date):
    """
        select date
    """
    time.sleep(2)
    base_node = base_node.find_element_by_xpath('.//*[@class="right-wrapper" and not(contains(@style, "none"))]')
    next_year = base_node.find_element_by_xpath('.//*[@aria-label="下一年"]')
    pre_year = base_node.find_element_by_xpath('.//*[@aria-label="上一年"]')
    next_month = base_node.find_element_by_xpath('.//*[@aria-label="下个月"]')
    pre_month = base_node.find_element_by_xpath('.//*[@aria-label="上个月"]')
    cur_year = base_node.find_element_by_xpath('.//*[@class="veui-calendar-left"]//b').text
    cur_month = base_node.find_element_by_xpath('.//*[@class="veui-calendar-right"]//b').text
    diff_year = int(cur_year) - date.year
    diff_month = int(cur_month) - date.month
    if diff_year > 0:
        for _ in range(abs(diff_year)):
            pre_year.click()
    elif diff_year < 0:
        for _ in range(abs(diff_year)):
            next_year.click()

    if diff_month > 0:
        for _ in range(abs(diff_month)):
            pre_month.click()
    elif diff_month <0:
        for _ in range(abs(diff_month)):
            next_month.click()

    time.sleep(1)
    base_node.find_elements_by_xpath('.//table//*[contains(@class, "veui-calendar-day")]')[date.day-1].click()


def get_index(keyword):
    """
        get index datas by html
    """
    # time.sleep(3)
    while True:
        try:
            date = browser.find_element_by_xpath('//*[@class="index-trend-chart"]/div[2]/div[1]').text
            date = date.split(' ')[0]
            index = browser.find_element_by_xpath('//*[@class="index-trend-chart"]/div[2]/div[2]/div[2]').text
            index = index.replace(',', '').strip(' ')
            break
        except (common.exceptions.NoSuchElementException,common.exceptions.StaleElementReferenceException):
            time.sleep(.5)
    #result = pd.DataFrame(columns=('word', 'date', 'index'))
    result = {
        'keyword': keyword,
        'date': date,
        'index': index,
    }
    return result


def loop_move(all_days, keyword):
    """
        to get the index by moving mouse
    """
    # time.sleep(2)
    while True:
        try:
            chart = browser.find_element_by_xpath('//*[@class="index-trend-chart"]')
            break
        except common.exceptions.NoSuchElementException:
            time.sleep(.5)
    chart_size = chart.size
    move_step = all_days - 1
    step_px = chart_size['width'] / move_step
    cur_offset = {
        'x': 1,
        'y': chart_size['height'] - 50
    }
    for _ in range(all_days):
        # time.sleep(0.05)
        webdriver.ActionChains(browser).move_to_element_with_offset(
            chart, int(cur_offset['x']), cur_offset['y']).perform()
        cur_offset['x'] += step_px
        yield get_index(keyword)


def get_baidu_index(keyword, startdate, enddate):
    init_browser()
    status = get_into_page(keyword)
    if status == 1:
        print('%s 关键词未被收录' % keyword)
        browser.quit()
        return None

    startdate, enddate = pd.to_datetime(startdate), pd.to_datetime(enddate)
    all_days = (enddate - startdate) // pd.offsets.Day(1)
    adjust_time_range(startdate, enddate)
    time.sleep(2)
    data_list = []
    for data in loop_move(all_days, keyword):
        data_list.append(data)
        # print(data)
    baidu_index = pd.DataFrame(data_list)
    browser.quit()

    # 结果整理
    baidu_index = baidu_index[baidu_index['index'] != '']
    baidu_index['date'] = pd.to_datetime(baidu_index['date'])
    baidu_index['index'] = baidu_index['index'].astype(int)
    baidu_index = baidu_index[['keyword','date','index']]

    return baidu_index


if __name__ == '__main__':
    keyword, startdate, enddate = '000001','20181001','20181106'
    baidu_index = get_baidu_index(keyword, startdate, enddate)
