# -*- coding: utf-8 -*-
'''
Created on 2014年4月25日

@author: y00752450
'''

from common_function import *
import app_category

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.markers as mk
import matplotlib.cm as mplcm
import matplotlib.colors as colors

def getAppDistributionOnMobility(dcPaths, mobility_indicator='cell'):
    '''
        Params:
                dcPaths - raw dcPaths
                mobility_indicator = use'cell' or 'org' as mobility indicator
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
            mobility = int(calculateRog(path) / 1000.0) # change unit to km, and round up
        else:
            print("unknown mobility indicator")
        
        # user number
        dcAppUserForCurrentMobility = dcAppUserPerMobility.get(mobility, None)
        if (None == dcAppUserForCurrentMobility):
            dcAppUserForCurrentMobility = {}
            dcAppUserPerMobility[mobility] = dcAppUserForCurrentMobility
        
        dcAppUserForCurrentUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dcAppUserForCurrentUser[app.m_nServiceType] = 1
        
        for tp in dcAppUserForCurrentUser.items():
            updateDictBySum(dcAppUserForCurrentMobility, tp[0], tp[1])
            
        # traffic
        dcAppTrafficForCurrentMobility = dcAppTrafficPerMobility.get(mobility, None)
        if (None == dcAppTrafficForCurrentMobility):
            dcAppTrafficForCurrentMobility = {}
            dcAppTrafficPerMobility[mobility] = dcAppTrafficForCurrentMobility
        
        for node in path.m_lsNodes:
            updateDictBySumOnAttribute(dcAppTrafficForCurrentMobility, node.m_lsApps, "m_nDownBytes")
    
    dfAppUserPerMobility = pd.DataFrame(dcAppUserPerMobility)
    dfAppTrafficPerMobility = pd.DataFrame(dcAppTrafficPerMobility) 
    
    return dfAppUserPerMobility, dfAppTrafficPerMobility

def getCategoryDistributionOnMobility(dfAppUserPerMobility, dfAppTrafficPerMobility):
    '''
        calculate user & traffic distribution for each app category
        
        Return:
                dataframe formated as: rows = mobility, columns = categories
    '''
    dcCategoryUser = {}
    dcCategoryTraffic = {}
    
    for tp in app_category.g_dcCategory.items():
        dcCategoryUser[tp[0]] = dfAppUserPerMobility.loc[dfAppUserPerMobility.index.isin(tp[1])].sum(axis=0)
        dcCategoryTraffic[tp[0]] = dfAppTrafficPerMobility.loc[dfAppTrafficPerMobility.index.isin(tp[1])].sum(axis=0)
    
    dfCategoryUser = pd.DataFrame(dcCategoryUser)
    dfCategoryTraffic = pd.DataFrame(dcCategoryTraffic)
      
    return dfCategoryUser, dfCategoryTraffic

def getPerCapitaTrafficOnMobility(dfAppUserPerMobility, dfAppTrafficPerMobility):
    '''
        Return:
                series with format: {mobility: per capita traffic with this mobility}
    '''
    sTotalUserNumPerMobility = dfAppUserPerMobility.sum(axis=0)
    sTotalTrafficPerMobility = dfAppTrafficPerMobility.sum(axis=0)
    return sTotalTrafficPerMobility.div(sTotalUserNumPerMobility)

def correlateCategoryPerCapitaTrafficAndMobility(dfCategoryTraffic, dfCategoryUser):
    '''
        calculate the pearson correlation btw per capita traffic of each category and mobility
        
        Return:
                a dataframe containing the coefficient
    '''
    dfCategoryPerCapitaTraffic = (dfCategoryTraffic.div(dfCategoryUser)).iloc[:20] # only care about 0 ~ 20 cell or km
    dfCategoryPerCapitaTraffic['mobility'] = dfCategoryPerCapitaTraffic.index
    dfCoefficient = dfCategoryPerCapitaTraffic.corr()
    return dfCoefficient
    
    

def getCategoryMobility():
    pass

def drawCategoryMobility():
    pass

def drawAll(dfCategoryUserPerMobility, dfCategoryTrafficPerMobility, sPerCapitaTrafficPerMobility, strXLabel='# cells'):
    
    fig, axes =  plt.subplots(nrows=1, ncols=3)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    # access probability
    sUserPerMobility = dfCategoryUserPerMobility.sum(axis=1)
    dfCategoryAccessProb = dfCategoryUserPerMobility.div(sUserPerMobility, axis=0)
    dfCategoryAccessProb.plot(ax=axes[0], style=lsLineStyle, xlim=(0, 20) )
    axes[0].set_xlabel(strXLabel)
    axes[0].set_ylabel('access probability')
    
    # Traffic contribution
    sTrafficPerMobility = dfCategoryTrafficPerMobility.sum(axis=1)
    dfCategoryTrafficProb = dfCategoryTrafficPerMobility.div(sTrafficPerMobility, axis=0)
    dfCategoryTrafficProb.plot(ax=axes[1], style=lsLineStyle, xlim=(0, 50) )
    # set style
    axes[1].set_xlabel(strXLabel)
    axes[1].set_ylabel('traffic contribution')
    
    # per capita traffic
    sPerCapitaTrafficPerMobility.plot(ax=axes[2], kind='bar', xlim=(0, 50) )
    axes[2].set_xlabel(strXLabel)
    axes[2].set_ylabel('traffic contribution')
    
    
    
def drawAccessProbability(dfCategoryUserPerCell, dfCategoryUserPerRog):
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    # cell
    sUserPerMobility = dfCategoryUserPerCell.sum(axis=1)
    dfCategoryAccessProb = dfCategoryUserPerCell.div(sUserPerMobility, axis=0)
    
    # color
    nColorCount = len(dfCategoryAccessProb.index)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    ax0 = dfCategoryAccessProb.plot(ax=axes[0], style=lsLineStyle, xlim=(0, 20), legend=False, colormap=cm)
    axes[0].set_xlabel("# cells")
    axes[0].set_ylabel('access probability')
    
    # rog
    sUserPerMobility = dfCategoryUserPerRog.sum(axis=1)
    dfCategoryAccessProb = dfCategoryUserPerRog.div(sUserPerMobility, axis=0)

    ax1 = dfCategoryAccessProb.plot(ax=axes[1], style=lsLineStyle, xlim=(0, 20), legend=False, colormap=cm)
    axes[1].set_xlabel("radius of gyration (km)")
#     axes[1].set_ylabel('access probability')
    
    fig.legend(ax0.get_lines(), dfCategoryAccessProb.columns, 'upper center')
    plt.show()
    
def drawPerCapitaTraffic(sPerCapitaTrafficPerCell, sPerCapitaTrafficPerRog):
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    # cell
    (sPerCapitaTrafficPerCell/1024).plot(ax=axes[0], kind='bar', xlim=(0, 20))
    axes[0].set_xlabel("# cell")
    axes[0].set_ylabel('average traffic (KB)')
    
    # rog
#     axes[1].yaxis.tick_right()
    (sPerCapitaTrafficPerRog/1024).plot(ax=axes[1], kind='bar', xlim=(0, 20))
    axes[1].set_xlabel("radius of gyration (km)")
    axes[1].set_ylabel('average traffic (KB)')
    
#     axes[1].set_ylabel('traffic contribution')
    
    plt.show()
    
    
    
def drawTrafficContribution(dfCategoryTrafficPerCell, dfCategoryTrafficPerRog):
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    # cell
    sTrafficPerMobility = dfCategoryTrafficPerCell.sum(axis=1)
    dfCategoryTrafficProb = dfCategoryTrafficPerCell.div(sTrafficPerMobility, axis=0)
    
    # color
    nColorCount = len(dfCategoryTrafficProb.index)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    
    ax0 = dfCategoryTrafficProb.plot(ax=axes[0], style=lsLineStyle, xlim=(0, 20), legend=False , colormap=cm)
    axes[0].set_xlabel("# cells")
    axes[0].set_ylabel('traffic contribution')
    
    # rog
    sTrafficPerMobility = dfCategoryTrafficPerRog.sum(axis=1)
    dfCategoryTrafficProb = dfCategoryTrafficPerRog.div(sTrafficPerMobility, axis=0)
    
    ax1 = dfCategoryTrafficProb.plot(ax=axes[1], style=lsLineStyle, xlim=(0, 20), legend=False, colormap=cm)
    axes[1].set_xlabel("radius of gyration (km)")
#     axes[1].set_ylabel('traffic contribution')
    
    fig.legend(ax0.get_lines(), dfCategoryTrafficProb.columns, 'upper center')
    plt.show()
    
def getAvgTrafficSDPerMobility(dcPaths, sPerCapitaTrafficPerMobility, mobility_indicator='cell'):
    '''
        this function calculate standard deviation of average traffic per mobility
    '''
    
    dcDeviationSumPerMobility = {}
    dcUserNumPerMobility = {}
    
    for path in dcPaths.values():
        mobility = 0
        if('cell' == mobility_indicator):
            mobility = len(path.m_lsNodes)
        elif ('rog' == mobility_indicator):
            mobility = int(calculateRog(path) / 1000.0) # change unit to km, and round up
        else:
            print("unknown mobility_indicator")
            
        dTraffic = 0.0
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dTraffic += app.m_nDownBytes
                
        dAvgTraffic = sPerCapitaTrafficPerMobility.loc[mobility]
        
        updateDictBySum(dcDeviationSumPerMobility, mobility, pow((dTraffic-dAvgTraffic), 2) )
        updateDictBySum(dcUserNumPerMobility, mobility, 1.0) 
        
    sDeviationSumPerMobility = pd.Series(dcDeviationSumPerMobility)
    sUserNumPerMobility = pd.Series(dcUserNumPerMobility)
    sSDPerMobility = sDeviationSumPerMobility.div(sUserNumPerMobility)
    
    sSDPerMobility.apply(np.sqrt)
    
    return sSDPerMobility.apply(np.sqrt)
        

def execute(dcPaths):
    '''
        include measurements on:
            1. access probability of each app vs. mobility
            2. traffic contribution of each app vs. mobility
            3. per capita traffic of each app vs. mobility
    '''
    
    nCellLim = 20
    nRogLim = 21
    
    # mobility on cell
    print("mobility = #cell")
    dfAppUserPerCell, dfAppTrafficPerCell = getAppDistributionOnMobility(dcPaths, mobility_indicator='cell')
    dfCategoryUserPerCell, dfCategoryTrafficPerCell = \
     getCategoryDistributionOnMobility(dfAppUserPerCell, dfAppTrafficPerCell)
    sPerCapitaTrafficPerCell = getPerCapitaTrafficOnMobility(dfAppUserPerCell, dfAppTrafficPerCell)
#     sAvgTrafficSDPerCell = getAvgTrafficSDPerMobility(dcPaths, sPerCapitaTrafficPerCell, 'cell')
    
    
    # mobility on rog
    print("mobility = rog")
    dfAppUserPerRog, dfAppTrafficPerRog = getAppDistributionOnMobility(dcPaths, mobility_indicator='rog')
    dfCategoryUserPerRog, dfCategoryTrafficPerRog = \
     getCategoryDistributionOnMobility(dfAppUserPerRog, dfAppTrafficPerRog)
    sPerCapitaTrafficPerRog = getPerCapitaTrafficOnMobility(dfAppUserPerRog, dfAppTrafficPerRog)
#     sAvgTrafficSDPerRog = getAvgTrafficSDPerMobility(dcPaths, sPerCapitaTrafficPerRog, 'rog')
    
    
    # draw
    drawPerCapitaTraffic(sPerCapitaTrafficPerCell.iloc[:nCellLim], sPerCapitaTrafficPerRog.iloc[:nRogLim])
    
    drawAccessProbability(dfCategoryUserPerCell.iloc[:nCellLim], dfCategoryUserPerRog.iloc[:nRogLim])
    
    drawTrafficContribution(dfCategoryTrafficPerCell.iloc[:nCellLim], dfCategoryTrafficPerRog.iloc[:nRogLim])
    

