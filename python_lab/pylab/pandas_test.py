# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import common_statistics as st
from node import *

def aggregateData(dcPaths, key="cell"):
    '''
        key=cell -> rearrange paths by cell ID
        key=app  -> reaggregated paths by app ID
    '''
    # TODO: add support for aggregation by app
    if(key == "app"):
        raise StandardError("Unsupported key, haven't done yet")
    dcAggregated = {}
    for path in dcPaths:
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            cell = dcAggregated.get(strKey)
            if (None == cell):
                cell = CNode("Aggregated", node.m_nLac, node.m_nCellID)
            value = mergeNodes([cell, node])
            dcAggregated.update((strKey, value) )
    
    return dcAggregated


if __name__ == '__main__':
    # load data
#     col_name = ['rank', \
#                 'qq.ci', 'qq.bytes', 'qq.u_num',\
#                 'taobao.ci', 'taobao.bytes', 'taobao.u_num',\
#                 'http.ci', 'http.bytes', 'http.u_num',\
#                 'ppstream.ci', 'ppstream.bytes', 'ppstream.u_num',
#                 'sina_weibo.ci', 'sina_weibo.bytes', 'sina_weibo.u_num',\
#                 'baidumap.ci', 'baidumap.bytes', 'baidumap.u_num']

#     col_name = ['ci', 'u_num', 'd_bytes', 'lat', 'long']
    qq_data = pd.read_csv("../../../../playground/cell_location_qq.csv")
    http_data = pd.read_csv("../../../../playground/cell_location_http.csv")
    ppstream_data = pd.read_csv("../../../../playground/cell_location_ppstream.csv")
    pop3_data = pd.read_csv("../../../../playground/cell_location_pop3.csv")
    sinaweibo_data = pd.read_csv("../../../../playground/cell_location_sinaweibo.csv")
    taobao_data = pd.read_csv("../../../../playground/cell_location_taobao_real.csv")
    baidumap_data = pd.read_csv("../../../../playground/cell_location_baidumap_real.csv")
    youku_data = pd.read_csv("../../../../playground/cell_location_youku.csv")
    game_data = pd.read_csv("../../../../playground/cell_location_chinagamecenter.csv")

    total_data = pd.DataFrame({'qq.ci':qq_data['ci'],\
                               'qq.u_num':qq_data['u_num'],\
                               'qq.d_bytes':qq_data['d_bytes'],\
                               'http.ci':http_data['ci'],\
                               'http.u_num':http_data['u_num'],\
                               'http.d_bytes':http_data['d_bytes'],\
                               'ppstream.ci':ppstream_data['ci'],\
                               'ppstream.u_num':ppstream_data['u_num'],\
                               'ppstream.d_bytes':ppstream_data['d_bytes'],\
                               'pop3.ci':pop3_data['ci'],\
                               'pop3.u_num':pop3_data['u_num'],\
                               'pop3.d_bytes':pop3_data['d_bytes'],\
                               'sinaweibo.ci':sinaweibo_data['ci'],\
                               'sinaweibo.u_num':sinaweibo_data['u_num'],\
                               'sinaweibo.d_bytes':sinaweibo_data['d_bytes'],\
                               'taobao.ci':taobao_data['ci'],\
                               'taobao.u_num':taobao_data['u_num'],\
                               'taobao.d_bytes':taobao_data['d_bytes'],\
                               'baidumap.ci':baidumap_data['ci'],\
                               'baidumap.u_num':baidumap_data['u_num'],\
                               'baidumap.d_bytes':baidumap_data['d_bytes'],\
                               'youku.ci':youku_data['ci'],\
                               'youku.u_num':youku_data['u_num'],\
                               'youku.d_bytes':youku_data['d_bytes'],\
                               'game.ci':game_data['ci'],\
                               'game.u_num':game_data['u_num'],\
                               'game.d_bytes':game_data['d_bytes']
                                })
    st.drawCDF(total_data[['qq.d_bytes', 'http.d_bytes', 'taobao.d_bytes','ppstream.d_bytes','sinaweibo.d_bytes','baidumap.d_bytes', 'youku.d_bytes', 'game.d_bytes']], \
    0, 5000, 500, "Downlink Traffic CDF")

    #st.drawCDF(total_data[['qq.u_num', 'http.u_num', 'taobao.u_num','ppstream.u_num','sinaweibo.u_num','baidumap.u_num', 'youku.u_num', 'game.u_num']], \
    #0, 5000, 500, "User Number CDF")

    plt.show()






