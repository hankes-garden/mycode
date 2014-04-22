# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jason
'''

import pandas as pd
import matplotlib.pyplot as plt

def getAppCategoryUserNum(sAppUser, bDraw=False):
    dcAppCategoryUser = {}
    dcAppCategoryUser['web_browsing'] = sAppUser.loc[1002:1006].sum()
    dcAppCategoryUser['p2p_downloading'] = sAppUser.loc[2001:2037].sum()
    dcAppCategoryUser['instant_message'] = sAppUser.loc[3001:3029].sum()
    dcAppCategoryUser['reading'] = sAppUser.loc[4001:4016].sum()
    dcAppCategoryUser['social_network'] = sAppUser.loc[5001:5005].sum()
    dcAppCategoryUser['social_network'] += sAppUser.loc[21001:21010].sum()
    dcAppCategoryUser['video'] = sAppUser.loc[6001:7004].sum()
    dcAppCategoryUser['music'] = sAppUser.loc[8001:8016].sum()
    dcAppCategoryUser['app_market'] = sAppUser.loc[9001:9003].sum()
    dcAppCategoryUser['game'] = sAppUser.loc[10001:10115].sum()
    dcAppCategoryUser['email'] = sAppUser.loc[11001:11017].sum()
    dcAppCategoryUser['stock'] = sAppUser.loc[16001:16012].sum()
    dcAppCategoryUser['shopping'] = sAppUser.loc[22001:22006].sum()
    dcAppCategoryUser['map'] = sAppUser.loc[26001:26003].sum()
    sAppCategoryUser = pd.Series(dcAppCategoryUser)
    
    if(True == bDraw):
        plt.figure()
        sAppCategoryUser.plot(kind='bar')
        plt.legend(loc='best')
        plt.show()
    
    return sAppCategoryUser


def getAppCategoryTraffic(dfAgg, bDraw=False):
    dcAppCategoryTraffic = {}
    dcAppCategoryTraffic['web_browsing'] = dfAgg.loc[1002:1006].sum(axis=1).sum()
    dcAppCategoryTraffic['p2p_downloading'] = dfAgg.loc[2001:2037].sum(axis=1).sum()
    dcAppCategoryTraffic['instant_message'] = dfAgg.loc[3001:3029].sum(axis=1).sum()
    dcAppCategoryTraffic['reading'] = dfAgg.loc[4001:4016].sum(axis=1).sum()
    dcAppCategoryTraffic['social_network'] = dfAgg.loc[5001:5005].sum(axis=1).sum()
    dcAppCategoryTraffic['social_network'] += dfAgg.loc[21001:21010].sum(axis=1).sum()
    dcAppCategoryTraffic['video'] = dfAgg.loc[6001:7004].sum(axis=1).sum()
    dcAppCategoryTraffic['music'] = dfAgg.loc[8001:8016].sum(axis=1).sum()
    dcAppCategoryTraffic['app_market'] = dfAgg.loc[9001:9003].sum(axis=1).sum()
    dcAppCategoryTraffic['game'] = dfAgg.loc[10001:10115].sum(axis=1).sum()
    dcAppCategoryTraffic['email'] = dfAgg.loc[11001:11017].sum(axis=1).sum()
    dcAppCategoryTraffic['stock'] = dfAgg.loc[16001:16012].sum(axis=1).sum()
    dcAppCategoryTraffic['shopping'] = dfAgg.loc[22001:22006].sum(axis=1).sum()
    dcAppCategoryTraffic['map'] = dfAgg.loc[26001:26003].sum(axis=1).sum()
    sAppCategoryTraffic = pd.Series(dcAppCategoryTraffic)
    
    if(True == bDraw):
        plt.figure()
        sAppCategoryTraffic.plot(kind='bar')
        plt.legend(loc='best')
        plt.show()
        
    return sAppCategoryTraffic
        
def getAppCategoryUserPerHour():
    pass
        
def getAppCategoryCorrelation():
    pass

if __name__ == '__main__':
    pass