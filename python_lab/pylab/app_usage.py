# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jason
'''

import pandas as pd
import matplotlib.pyplot as plt

import app_category

def getCategoryUserNum(sAppUser):
    '''
        return a series {'category':#user} 
    '''
    dcAppCategoryUser = {}
    
    for tp in app_category.g_dcCategory.items():
        dcAppCategoryUser[tp[0]] = \
            sAppUser.loc[sAppUser.index.isin(tp[1])].sum()
    
    sAppCategoryUser = pd.Series(dcAppCategoryUser)
    
    return sAppCategoryUser


def getCategoryTraffic(dfAgg):
    '''
        return a series{'category':traffic_percentage}
    '''
    nTotalTraffic = dfAgg.sum().sum()
    dcAppCategoryTraffic = {}
    dcAppCategoryTraffic['web_browsing'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsWebBrowsing)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['p2p'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsP2P)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['im'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsIM)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['reading'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsReading)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['social_network'] \
    = dfAgg.loc[dfAgg.index.isin(app_category.g_lsSNS)].sum(axis=1).sum()/nTotalTraffic
  
    dcAppCategoryTraffic['video'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsVideo)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['music'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsMusic)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['app_market'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsAppMarket)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['game'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsGame)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['email'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsEmail)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['stock'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsStock)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['shopping'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsShopping)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['map'] = \
    dfAgg.loc[dfAgg.index.isin(app_category.g_lsMap)].sum(axis=1).sum()/nTotalTraffic
    
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
    axes[0].set_xlabel('a. # uniqure users of app categories')
    axes[1].set_ylabel('traffic volume (%)')
    axes[1].set_xlabel('b. normalized traffic volume of app categories')
        
def getAppCategoryUserPerHour():
    pass
        
def getAppCategoryCorrelation():
    pass

def drawCategoryTrafficDynamics():
    pass

def execute(sAppUserNum, dfCleanedData):
    sCategoryUserNum = getCategoryUserNum(sAppUserNum)
    sCategoryTraffic = getCategoryTraffic(dfCleanedData)
    drawCategoryPopularity(sCategoryUserNum, sCategoryTraffic)

if __name__ == '__main__':
    pass
