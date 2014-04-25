# -*- coding: utf-8 -*-
'''
Created on 2014年4月25日

@author: y00752450
'''

from common_function import *
import app_category

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.markers as mk

def getAppDistributionOnMobility(dcPaths):
    '''
        return a dataframe like:
            row = app
            col = mobility
    '''
    dcAppUserPerMobility = {}
    dcAppTrafficPerMobility = {}
    
    for path in dcPaths.values():
        mobility = len(path.m_lsNodes)
        
        # user number
        dcAppUserOnCurrentMobility = dcAppUserPerMobility.get(mobility, None)
        if (None == dcAppUserOnCurrentMobility):
            dcAppUserOnCurrentMobility = {}
            dcAppUserPerMobility[mobility] = dcAppUserOnCurrentMobility
        
        dcAppUserForCurrentUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dcAppUserForCurrentUser[app.m_nServiceType] = 1
        
        for tp in dcAppUserForCurrentUser.items():
            updateDictBySum(dcAppUserOnCurrentMobility, tp[0], tp[1])
            
        # traffic
        dcAppTrafficOnCurrentMobility = dcAppTrafficPerMobility.get(mobility, None)
        if (None == dcAppTrafficOnCurrentMobility):
            dcAppTrafficOnCurrentMobility = {}
            dcAppTrafficPerMobility[mobility] = dcAppTrafficOnCurrentMobility
        
        for node in path.m_lsNodes:
            updateDictBySumOnAttribute(dcAppTrafficOnCurrentMobility, node.m_lsApps, "m_nDownBytes")
    
    dfAppUserPerMobility = pd.DataFrame(dcAppUserPerMobility)
    dfAppTrafficPerMobility = pd.DataFrame(dcAppTrafficPerMobility) 
    
    return dfAppUserPerMobility, dfAppTrafficPerMobility

def getCategoryDistributionOnMobility(dfAppUserPerMobility, dfAppTrafficPerMobility):
    
    dcCategoryUser = {}
    dcCategoryTraffic = {}
    
    for tp in app_category.g_dcCategory.items():
        dcCategoryUser[tp[0]] = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(tp[1])].sum(axis=0)
        dcCategoryTraffic[tp[0]] = dfAppTrafficPerMobility.loc[dfAppTrafficPerMobility.index.isin(tp[1])].sum(axis=0)
    
#     sUserWebBrowsing = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsWebBrowsing)].sum(axis=0)
#     sUserP2P = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsP2P)].sum(axis=0)
#     sUserIM = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsIM)].sum(axis=0)
#     sUserReading = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsReading)].sum(axis=0)
#     sUserSNS = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsSNS)].sum(axis=0)
#     sUserVideo = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsVideo)].sum(axis=0)
#     sUserMusic = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsMusic)].sum(axis=0)
#     sUserAppMarket = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsAppMarket)].sum(axis=0)
#     sUserGame = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsGame)].sum(axis=0)
#     sUserEmail = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsEmail)].sum(axis=0)
#     sUserStock = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsStock)].sum(axis=0)
#     sUserShopping = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsShopping)].sum(axis=0)
#     sUserMap = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(app_category.g_lsMap)].sum(axis=0)
#     
#     
#     dfCategoryUser[app_category.g_strWebBrowsing] = sUserWebBrowsing
#     dfCategoryUser[app_category.g_strP2P] = sUserP2P
#     dfCategoryUser[app_category.g_strIM] = sUserIM
#     dfCategoryUser[app_category.g_strReading] = sUserReading
#     dfCategoryUser[app_category.g_strSNS] = sUserSNS
#     dfCategoryUser[app_category.g_strVideo] = sUserVideo
#     dfCategoryUser[app_category.g_strMusic] = sUserMusic
#     dfCategoryUser[app_category.g_strAppMarket] = sUserAppMarket
#     dfCategoryUser[app_category.g_strGame] = sUserGame
#     dfCategoryUser[app_category.g_strEmail] = sUserEmail
#     dfCategoryUser[app_category.g_strStock] = sUserStock
#     dfCategoryUser[app_category.g_strShopping] = sUserShopping
#     dfCategoryUser[app_category.g_strMap] = sUserMap
    
    dfCategoryUser = pd.DataFrame(dcCategoryUser)
    dfCategoryTraffic = pd.DataFrame(dcCategoryTraffic)
    
    return dfCategoryUser, dfCategoryTraffic
    
    

def drawCategoryAccessProbability(dfCategoryUserPerMobility):
    sUserPerMobility = dfCategoryUserPerMobility.sum(axis=1)
    dfCategoryAccessProb = dfCategoryUserPerMobility.div(sUserPerMobility, axis=0)
    
    ax0 =  plt.subplot()
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    dfCategoryAccessProb.plot(ax=ax0, style=lsLineStyle, xlim=(0, 20) )
    # set style
    ax0.set_xlabel('# cells')
    ax0.set_ylabel('access probability')

def drawCategoryTrafficProbability(dfCategoryTrafficPerMobility):
    sTrafficPerMobility = dfCategoryTrafficPerMobility.sum(axis=1)
    dfCategoryTrafficProb = dfCategoryTrafficPerMobility.div(sTrafficPerMobility, axis=0)
    
    ax0 = plt.subplot()
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    dfCategoryTrafficProb.plot(ax=ax0, style=lsLineStyle, xlim=(0, 50) )
    # set style
    ax0.set_xlabel('# cells')
    ax0.set_ylabel('traffic contribution')

def getCategoryMobility():
    pass

def drawCategoryMobility():
    pass

def execute(dcPaths):
    dfAppUserPerMobility, dfAppTrafficPerMobility = getAppDistributionOnMobility(dcPaths)
    dfCategoryUser, dfCategoryTraffic = \
     getCategoryDistributionOnMobility(dfAppUserPerMobility, dfAppTrafficPerMobility)
    drawCategoryAccessProbability(dfCategoryUser)
    drawCategoryTrafficProbability(dfCategoryTraffic)

