# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jason
'''

import pandas as pd
import matplotlib.pyplot as plt


def getAppCategoryUserNum(sAppUser):
    '''
        return a series {'category':#user} 
    '''
    dcAppCategoryUser = {}
    try:
        
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
        
    except KeyError as err:
        print("Ignore: " + err)
        pass
    
    sAppCategoryUser = pd.Series(dcAppCategoryUser)
    
    return sAppCategoryUser


def getAppCategoryTraffic(dfAgg):
    '''
        return a series{'category':traffic_percentage}
    '''
    nTotalTraffic = dfAgg.sum().sum()
    dcAppCategoryTraffic = {}
    dcAppCategoryTraffic['web_browsing'] = dfAgg.loc[1002:1006].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['p2p_downloading'] = dfAgg.loc[2001:2037].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['instant_message'] = dfAgg.loc[3001:3029].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['reading'] = dfAgg.loc[4001:4016].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['social_network'] = dfAgg.loc[5001:5005].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['social_network'] += dfAgg.loc[21001:21010].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['video'] = dfAgg.loc[6001:7004].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['music'] = dfAgg.loc[8001:8016].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['app_market'] = dfAgg.loc[9001:9003].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['game'] = dfAgg.loc[10001:10115].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['email'] = dfAgg.loc[11001:11017].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['stock'] = dfAgg.loc[16001:16012].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['shopping'] = dfAgg.loc[22001:22006].sum(axis=1).sum()/nTotalTraffic
    dcAppCategoryTraffic['map'] = dfAgg.loc[26001:26003].sum(axis=1).sum()/nTotalTraffic
    sAppCategoryTraffic = pd.Series(dcAppCategoryTraffic)


    return sAppCategoryTraffic
    
def drawCategoryPopularity(sAppCategoryUserNum, sAppCategoryTraffic):
    '''
        draw user_num & traffic_percentage of different app categories
    '''
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    sAppCategoryUserNum.plot(ax=axes[0], kind='bar')
    sAppCategoryTraffic.plot(ax=axes[1], kind='bar')
    
    axes[0].set_ylabel('# unique users')
    axes[0].set_ylabel('traffic volume (%)')
        
        
def getAppCategoryUserPerHour():
    pass
        
def getAppCategoryCorrelation():
    pass

def drawCategoryTrafficDynamics():
    pass

if __name__ == '__main__':
    pass