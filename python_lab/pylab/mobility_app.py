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

def getAppDistributionOnMobility(dcPaths, mobility_indicator='cell'):
    '''
        Params:
                dcPaths - raw dcPaths
                mobility_indicator = use'cell' or 'org' as mobility indictor
        Return:
                Two dataframe:dfAppUserPerMobility, dfAppTrafficPerMobility
                both format like: row = app, and col = mobility
    '''
    dcAppUserPerMobility = {}
    dcAppTrafficPerMobility = {}
    
    for path in dcPaths.values():
        
        mobility = 0
        if('cell' == mobility_indicator):
            mobility = len(path.m_lsNodes)
        elif ('rog' == mobility_indicator):
            mobility = calculateRog(path) / 1000.0 # change unit to km
        
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
    
    # mobility on cell
    dfAppUserPerCell, dfAppTrafficPerCell = getAppDistributionOnMobility(dcPaths, mobility_indicator='cell')
    dfCategoryUserPerCell, dfCategoryTrafficPerCell = \
     getCategoryDistributionOnMobility(dfAppUserPerCell, dfAppTrafficPerCell)
    
    # mobility on rog
    dfAppUserPerRog, dfAppTrafficPerRog = getAppDistributionOnMobility(dcPaths, mobility_indicator='rog')
    dfCategoryUserPerRog, dfCategoryTrafficPerRog = \
     getCategoryDistributionOnMobility(dfAppUserPerRog, dfAppTrafficPerRog)
     
    # draw
    drawCategoryAccessProbability(dfCategoryUserPerCell)
    drawCategoryTrafficProbability(dfCategoryTrafficPerCell)
    
    drawCategoryAccessProbability(dfCategoryUserPerRog)
    drawCategoryTrafficProbability(dfCategoryTrafficPerRog)

