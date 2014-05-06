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
    
    for tp in app_category.g_dcCategory.items():
        dcAppCategoryTraffic[tp[0]] = \
            dfAgg.loc[dfAgg.index.isin(tp[1])].sum(axis=1).sum()/nTotalTraffic
    
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
    
    plt.show()
        
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
