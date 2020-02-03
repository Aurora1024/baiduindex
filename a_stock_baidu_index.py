"提取A股股票相关的百度指数"


import os
import numpy as np
import pandas as pd
from time import clock
from sqlalchemy import create_engine
from multiprocessing import Pool
from get_baidu_index import get_baidu_index

mysql_url = "mysql+pymysql://admin:Dfjg0026@192.168.1.83/factor?charset=gbk"


def get_stock_names():
    "股票名称"
    engine = create_engine(mysql_url)
    query = """
    SELECT LEFT(S_INFO_WINDCODE, 6) as stockcode, S_INFO_NAME as stockname
    FROM wind_filesync.asharedescription
    WHERE S_INFO_LISTDATE IS NOT NULL
    """
    stockname = pd.read_sql(query, engine, index_col=['stockcode'])['stockname']
    stocknames = stockname.apply(lambda s: s.replace('*','').replace('(退市)',''))

    return stocknames


def get_ui_stock_idx(indexcode='000300.SH'):
    "样本空间涉及的股票数量集"

    engine = create_engine(mysql_url)
    query = """
    SELECT DISTINCT LEFT(S_CON_WINDCODE, 6) as stockcode
    FROM wind_filesync.aindexmembers
    WHERE S_INFO_WINDCODE = '%s'
    """ % indexcode
    stockcode = pd.read_sql(query, engine)['stockcode'].values

    return pd.Index(stockcode)


def get_baidu_index_by_keyword(keyword):
    "提取关键词整个时间序列的百度指数, 并输出至csv文件"
    t1 = clock()

    # 开始结束日期
    dt_nodes = pd.date_range('20101231','20181105',freq='Q') + pd.offsets.Day(1)
    dt_nodes = dt_nodes.append(pd.to_datetime(['20181105']))

    # bi_list = []
    for start, end in zip(dt_nodes[:-1],dt_nodes[1:]):
        t2 = clock()
        fpath = '指数数据/{0}_{1}.csv'.format(keyword,start.strftime('%Y%m%d'))
        if os.path.exists(fpath):
            continue
        try:
            bi = get_baidu_index(keyword, start, end)
        except:
            continue
        print(keyword, start.strftime('%Y%m%d'), '%.2f seconds.' % (clock()-t2))
        if bi is None:
            bi = pd.DataFrame(columns=['keyword','date','index'])
            for dt in dt_nodes[:-1]:
                fpath = '指数数据/{0}_{1}.csv'.format(keyword,dt.strftime('%Y%m%d'))
                bi.to_csv(fpath, index=False)
            print(keyword, 'error. %.2f seconds.' % (clock()-t1))
            return None
        else:
            bi = bi.sort_values('date')[['keyword','date','index']]
            bi.to_csv(fpath, index=False)

        # bi_list.append(bi)
    # bi = pd.concat(bi_list)
    # bi = bi.groupby(by=['keyword','date']).mean().sort_index()

    # # 输出
    # bi.to_csv('指数数据/%s.csv' % keyword)
    # print(keyword, 'done. %.2f seconds.' % (clock()-t1))


if __name__ == '__main__':
    t0 = clock()
    # 工作文件夹
    os.chdir("E:/百度指数/wukefei")

    # 需要下载的关键字
    stock_names = get_stock_names()
    idx = get_ui_stock_idx('000300.SH')
    kw_list = idx.tolist() + stock_names[idx].tolist()

    # 多进程下载数据
    pool = Pool(1)
    list(pool.map(get_baidu_index_by_keyword,kw_list))

    print('下载完成 共计 %.2f 分钟.' % ((clock()-t0)/60))
