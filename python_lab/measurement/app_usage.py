# -*- coding: utf-8 -*-
'''
Created on 2014年4月22日

@author: jason
'''

import pandas as pd
import matplotlib.pyplot as plt

import app_category
import data_loader
from my_error import *

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

def drawAppUserTrafficDistribution(sAppUser, sAppTraffic):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    sAppUser.sort(ascending=False)
    sAppUser.plot(ax=axes[0], style='-', use_index=False)
    
    sAppTraffic.sort(ascending=False)
    (sAppTraffic/1024.0).plot(ax=axes[1], style='-', use_index=False)
    
    axes[0].set_ylabel('# users')
    axes[0].set_xlabel('sorted app index')
    axes[1].set_ylabel('traffic volume (KB)')
    axes[1].set_xlabel('sorted app index')
    
    plt.show()
    
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

def execute(sAppUserNum = None, dfCleanedAppTraffic = None, dcPaths = None, strAttribName='m_nDownBytes', nTopApp = 200):
    '''
        This function computes and draws the user number and traffic volume of each app category 
        w.r.t. given dcPaths
        If No dcPaths is given, then the sAppUserNum & dfCleanedAppTraffic should not be None
    '''
    if (sAppUserNum is None or dfCleanedAppTraffic is None):
        if (dcPaths is None):
            raise MyError("dcPaths should not be None if sAppUserNum = None or dfCleanedAppTraffic = None.")
        
        dcData = {}
        dcAggAppNum = {}
        
        # traffic of each app: app_id v.s cell_id
        data_loader.aggregateDataInAppCellIncrementally(dcPaths, dcData)
    
        # user number of each app
        data_loader.aggregateAppUserNumIncrementally(dcPaths, dcAggAppNum)
        
        dfAgg = pd.DataFrame(dcData)
        sAppUserNum = pd.Series(dcAggAppNum)
    
        dfCleanedAppTraffic = data_loader.cleanData(dfAgg, sAppUserNum, nTopApp)
    
    drawAppUserTrafficDistribution(sAppUserNum, dfCleanedAppTraffic.sum(1))
    
    sCategoryUserNum = getCategoryUserNum(sAppUserNum)
    sCategoryTraffic = getCategoryTraffic(dfCleanedAppTraffic)
    drawCategoryPopularity(sCategoryUserNum, sCategoryTraffic)

