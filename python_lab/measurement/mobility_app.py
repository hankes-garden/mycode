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
                mobility_indicator = use'cell' or 'rog' as mobility indicator
        Return:
                dfAppUserPerMobility, dfAppTrafficPerMobility, both format like: row = app, and col = mobility
                srTotalUserPerMobility, row=mobility, column=total_user_number
        Note:
                When using rog as mobility indicator, some users' paths are not counted
                as the supporting ratio is too low, thus the total user number counted
                by rog can be smaller than the total number counted by #cell. Whenever
                using the result, be aware of it!
    '''
    
    dcTotalUserPerMobility = {}
    dcAppUserPerMobility = {}
    dcAppTrafficPerMobility = {}
    
    for path in dcPaths.values():
        #=======================================================================
        # compute mobility
        #=======================================================================
        mobility, dConfidenceRatio = computeSubscriberMobility(path, mobility_indicator)
        if (dConfidenceRatio < g_dMinConfidenceRatio):
            continue # mobility information is not convincing, skip it
        #=======================================================================
        # total user number
        #=======================================================================
        updateDictBySum(dcTotalUserPerMobility, mobility, 1)
        
        #=======================================================================
        # app user number, {mobility_value: {app1: user_number, ...}, ...}
        #=======================================================================
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
            
        #=======================================================================
        # traffic
        #=======================================================================
        dcAppTrafficForCurrentMobility = dcAppTrafficPerMobility.get(mobility, None)
        if (None == dcAppTrafficForCurrentMobility):
            dcAppTrafficForCurrentMobility = {}
            dcAppTrafficPerMobility[mobility] = dcAppTrafficForCurrentMobility
        
        for node in path.m_lsNodes:
            updateDictBySumOnAttribute(dcAppTrafficForCurrentMobility, node.m_lsApps, "m_nDownBytes")
    
    srTotalUserPerMobility = pd.Series(dcTotalUserPerMobility)
    dfAppUserPerMobility = pd.DataFrame(dcAppUserPerMobility)
    dfAppTrafficPerMobility = pd.DataFrame(dcAppTrafficPerMobility) 
    
    return srTotalUserPerMobility, dfAppUserPerMobility, dfAppTrafficPerMobility

def getCategoryDistributionOnMobility(dcPaths, mobility_indicator):
    '''
        This function computes user number and traffic distribution of 
        app categories on mobility
        
        param:
                dcPaths             - roaming paths
                mobility_indicator  - cell or rog
        return:
                dfCategoryUserPerMobility    - row:strCategoryName, col:mobility
                dfCategoryTrafficPerMobility - row:strCategoryName, col:mobility
                    
    '''
    
    dcCategoryUserPerMobility = {}
    dcCategoryTrafficPerMobility = {}
    
    for path in dcPaths.values():
        #=======================================================================
        # compute mobility
        #=======================================================================
        mobility, dConfidenceRatio = computeSubscriberMobility(path, mobility_indicator)
        if (dConfidenceRatio < g_dMinConfidenceRatio):
            continue # mobility information is not convincing, skip it
            
        #=======================================================================
        # Category user number, {mobility_value: {category_name: user_number, ...}, ...}
        #=======================================================================
        dcCategoryUserForCurrentMobility = dcCategoryUserPerMobility.get(mobility, None)
        if (dcCategoryUserForCurrentMobility is None):
            dcCategoryUserForCurrentMobility = {}
            dcCategoryUserPerMobility[mobility] = dcCategoryUserForCurrentMobility
        
        dcCategoryUserForCurrentUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                strCategoryName = app_category.getAppCategory(app.m_nServiceType)
                dcCategoryTrafficPerMobility[strCategoryName] = 1
        
        for (k,v) in dcCategoryUserForCurrentUser.iteritems():
            updateDictBySum(dcCategoryUserForCurrentMobility, k, v)
            
        #=======================================================================
        # category traffic = {mobility_value: {category_name: traffic_volume, ...}, ...}
        #=======================================================================
        dcCategoryTrafficForCurrentMobility = dcCategoryTrafficPerMobility.get(mobility, None)
        if (dcCategoryTrafficForCurrentMobility is None):
            dcCategoryTrafficForCurrentMobility = {}
            dcCategoryTrafficPerMobility[mobility] = dcCategoryTrafficForCurrentMobility
            
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                strCategoryName = app_category.getAppCategory(app.m_nServiceType)
                updateDictBySum(dcCategoryTrafficForCurrentMobility, strCategoryName, app.m_nDownBytes)
        
    dfCategoryUserPerMobility = pd.DataFrame(dcCategoryUserPerMobility)
    dfCategoryTrafficPerMobility = pd.DataFrame(dcCategoryTrafficPerMobility)
    
    return dfCategoryUserPerMobility, dfCategoryTrafficPerMobility
      

def getPerCapitaTrafficOnMobility(srTotalUserPerMobility, dfAppTrafficPerMobility):
    '''
        Computes average traffic per user of different mobility
        Params:
                dfAppUserPerMobility, dfAppTrafficPerMobility, both format like:
                row=app, column=mobility
        Return:
                series with format: {mobility: per capita traffic with this mobility}
    '''
    sTotalTrafficPerMobility = dfAppTrafficPerMobility.sum(axis=0)
    return sTotalTrafficPerMobility.div(srTotalUserPerMobility)

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
    '''
        Plot category access probability on mobility
        
        param:
                dfCategoryUserPerCell - already been sliced and transposed, row:mobility, col:category
                dfCategoryUserPerRog  - already been sliced and transposed, row:mobility, col:category
        
    '''
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    #===========================================================================
    # mobility = #cell
    #===========================================================================
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
    '''
        This function shows the relationship btw traffic and mobility
        
        param:
                sPerCapitaTrafficPerCell - already been sliced by mobility
                sPerCapitaTrafficPerRog  - already been sliced by mobility
    '''
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    # cell
    (sPerCapitaTrafficPerCell/1024).plot(ax=axes[0], kind='bar', xlim=(1, 19), ylim=(1500, 5000) )
    axes[0].set_xlabel("# cell")
    axes[0].set_ylabel('average traffic (KB)')
    
    # rog
#     axes[1].yaxis.tick_right()
    (sPerCapitaTrafficPerRog/1024).plot(ax=axes[1], kind='bar', xlim=(0, 20), ylim=(1500, 5000) )
    axes[1].set_xlabel("radius of gyration (km)")
    axes[1].set_ylabel('average traffic (KB)')
    
#     axes[1].set_ylabel('traffic contribution')
    
    plt.show()
    
    
    
def drawTrafficContribution(dfCategoryTrafficPerCell, dfCategoryTrafficPerRog):
    '''
        Note that dfCategoryTrafficPerCell, dfCategoryTrafficPerRog have already been sliced and tranposed
    '''
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    #===========================================================================
    # cell
    #===========================================================================
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
    
    #===========================================================================
    # rog
    #===========================================================================
    sTrafficPerMobility = dfCategoryTrafficPerRog.sum(axis=1)
    dfCategoryTrafficProb = dfCategoryTrafficPerRog.div(sTrafficPerMobility, axis=0)
    
    ax1 = dfCategoryTrafficProb.plot(ax=axes[1], style=lsLineStyle, xlim=(0, 20), legend=False, colormap=cm)
    axes[1].set_xlabel("radius of gyration (km)")
#     axes[1].set_ylabel('traffic contribution')
    
    fig.legend(ax0.get_lines(), dfCategoryTrafficProb.columns, 'upper center')
    plt.show()
    
def drawTrafficDistribution(dfCategoryTrafficPerCell, dfCategoryTrafficPerRog):
    '''
        This function draw the absolute traffic volume of each app cateogory on mobility
        
        param:
                dfCategoryTrafficPerCell - row:mobility, col:category
                dfCategoryTrafficPerRog  - row:mobility, col:category
                
    '''
    
    # test these 
    ax = plt.axes() 
    upper, lower = axes_broken_y(ax, ybounds=[-2., 2.9, 22.1, 30.]) 
    upper.plot(range(30), range(30)) 
    lower.plot(range(30), range(30)) 
    upper.set_ylabel('Data') 
    plt.show()
    # TODO: add truncated axis support
    
    
    fig, axes =  plt.subplots(nrows=1, ncols=2)
    
    tpMakers = mk.MarkerStyle().filled_markers
    lsLineStyle = [ ('-%s' % str(m) ) for m in tpMakers ]
    
    #===========================================================================
    # cell
    #===========================================================================
    # color
    nColorCount = len(dfCategoryTrafficPerCell.index)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    # axis
    upperPerCell, lowerPerCell = axes_broken_y(ax, ybounds=[0, 2000, 3000, 6000]) 
    
    
    ax0 = dfCategoryTrafficPerCell.plot(ax=axes[0], style=lsLineStyle, xlim=(0, 20), legend=False , colormap=cm)
    axes[0].set_xlabel("# cells")
    axes[0].set_ylabel('traffic contribution')
    
    #===========================================================================
    # rog
    #===========================================================================
    
    ax1 = dfCategoryTrafficPerRog.plot(ax=axes[1], style=lsLineStyle, xlim=(0, 20), legend=False, colormap=cm)
    axes[1].set_xlabel("radius of gyration (km)")
#     axes[1].set_ylabel('traffic contribution')
    
    fig.legend(ax0.get_lines(), dfCategoryTrafficPerRog.columns, 'upper center')
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
    
    nXLim = 20 # limitation on mobility
    
    #===========================================================================
    # mobility on cell
    #===========================================================================
    print("mobility = #cell")
    srTotalUserPerCell, dfAppUserPerCell, dfAppTrafficPerCell = getAppDistributionOnMobility(dcPaths, mobility_indicator='cell')
    
    dfCategoryUserPerCell, dfCategoryTrafficPerCell = \
     getCategoryDistributionOnMobility(dcPaths, g_strMobilityInCell)
     
    sPerCapitaTrafficPerCell = getPerCapitaTrafficOnMobility(srTotalUserPerCell, dfAppTrafficPerCell)
#     sAvgTrafficSDPerCell = getAvgTrafficSDPerMobility(dcPaths, sPerCapitaTrafficPerCell, 'cell')
    
    
    #===========================================================================
    # mobility on rog
    #===========================================================================
    print("mobility = rog")
    srTotalUserPerRog, dfAppUserPerRog, dfAppTrafficPerRog = getAppDistributionOnMobility(dcPaths, mobility_indicator='rog')
    dfCategoryUserPerRog, dfCategoryTrafficPerRog = \
     getCategoryDistributionOnMobility(dcPaths, g_strMobilityInRog)
    sPerCapitaTrafficPerRog = getPerCapitaTrafficOnMobility(srTotalUserPerRog, dfAppTrafficPerRog)
#     sAvgTrafficSDPerRog = getAvgTrafficSDPerMobility(dcPaths, sPerCapitaTrafficPerRog, 'rog')
    
    
    # draw
    drawPerCapitaTraffic(sPerCapitaTrafficPerCell.iloc[:nXLim], sPerCapitaTrafficPerRog.iloc[:nXLim+1])
    
    drawAccessProbability(dfCategoryUserPerCell.iloc[:,:nXLim].T, dfCategoryUserPerRog.T.iloc[:,:nXLim].T)
    
    drawTrafficDistribution(dfCategoryTrafficPerCell.iloc[:,:nXLim].T, dfCategoryTrafficPerRog.iloc[:,:nXLim].T)
    

