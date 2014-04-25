# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jason
'''

import pandas as pd
import matplotlib.pyplot as plt


def getCategoryUserNum(sAppUser):
    '''
        return a series {'category':#user} 
    '''
    dcAppCategoryUser = {}
    
    dcAppCategoryUser['web_browsing'] = \
    sAppUser.loc[(sAppUser.index>=1002) & (sAppUser.index<=1006) ].sum()
    
    dcAppCategoryUser['p2p_downloading'] = \
    sAppUser.loc[(sAppUser.index>=2001) & (sAppUser.index<=2037) ].sum()
    
    dcAppCategoryUser['im'] = \
    sAppUser.loc[(sAppUser.index>=3001) & (sAppUser.index<=3029)].sum()
    
    dcAppCategoryUser['reading'] = \
    sAppUser.loc[(sAppUser.index>=4001) & (sAppUser.index<=4016)].sum()
    
    dcAppCategoryUser['social_network'] = \
    sAppUser.loc[(sAppUser.index>=5001) & (sAppUser.index<=5005)].sum()
    
    dcAppCategoryUser['social_network'] += \
    sAppUser.loc[(sAppUser.index>=21001) & (sAppUser.index<=21010)].sum()
    
    dcAppCategoryUser['video'] = \
    sAppUser.loc[(sAppUser.index>=6001) & (sAppUser.index<=7004)].sum()
    
    dcAppCategoryUser['music'] = \
    sAppUser.loc[(sAppUser.index>=8001) & (sAppUser.index<=8016)].sum()
    
    dcAppCategoryUser['app_market'] = \
    sAppUser.loc[(sAppUser.index>=9001) & (sAppUser.index<=9003)].sum()
    
    dcAppCategoryUser['game'] = \
    sAppUser.loc[(sAppUser.index>=10001) & (sAppUser.index<=10115)].sum()
    
    dcAppCategoryUser['email'] = \
    sAppUser.loc[(sAppUser.index>=11001) & (sAppUser.index<=11017)].sum()\
    
    
    dcAppCategoryUser['stock'] = \
    sAppUser.loc[(sAppUser.index>=16001) & (sAppUser.index<=16012)].sum()
    
    dcAppCategoryUser['shopping'] = \
    sAppUser.loc[(sAppUser.index>=22001) & (sAppUser.index<=22006)].sum()
    
    dcAppCategoryUser['map'] = \
    sAppUser.loc[(sAppUser.index>=26001) & (sAppUser.index<=26003)].sum()
    
    sAppCategoryUser = pd.Series(dcAppCategoryUser)
    
    return sAppCategoryUser


def getCategoryTraffic(dfAgg):
    '''
        return a series{'category':traffic_percentage}
    '''
    nTotalTraffic = dfAgg.sum().sum()
    dcAppCategoryTraffic = {}
    dcAppCategoryTraffic['web_browsing'] = \
    dfAgg.loc[(dfAgg.index>=1002) & (dfAgg.index<=1006)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['p2p_downloading'] = \
    dfAgg.loc[(dfAgg.index>=2001) & (dfAgg.index<=2037)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['im'] = \
    dfAgg.loc[(dfAgg.index>=3001) & (dfAgg.index<=3029)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['reading'] = \
    dfAgg.loc[(dfAgg.index>=4001) & (dfAgg.index<=4016)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['social_network'] \
    = dfAgg.loc[(dfAgg.index>=5001) & (dfAgg.index<=5005)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['social_network'] += \
    dfAgg.loc[(dfAgg.index>=21001) & (dfAgg.index<=21010)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['video'] = \
    dfAgg.loc[(dfAgg.index>=6001) & (dfAgg.index<=7004)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['music'] = \
    dfAgg.loc[(dfAgg.index>=8001) & (dfAgg.index<=8016)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['app_market'] = \
    dfAgg.loc[(dfAgg.index>=9001) & (dfAgg.index<=9003)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['game'] = \
    dfAgg.loc[(dfAgg.index>=10001) & (dfAgg.index<=10115)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['email'] = \
    dfAgg.loc[(dfAgg.index>=11001) & (dfAgg.index<=11017)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['stock'] = \
    dfAgg.loc[(dfAgg.index>=16001) & (dfAgg.index<=16012)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['shopping'] = \
    dfAgg.loc[(dfAgg.index>=22001) & (dfAgg.index<=22006)].sum(axis=1).sum()/nTotalTraffic
    
    dcAppCategoryTraffic['map'] = \
    dfAgg.loc[(dfAgg.index>=26001) & (dfAgg.index<=26003)].sum(axis=1).sum()/nTotalTraffic
    
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
