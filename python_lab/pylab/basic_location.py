# -*- coding: utf-8 -*-
'''
Created on 2014年5月1日

@author: jason
'''

import region_type
from common_function import *
import app_category

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.markers as mk
from matplotlib.axis import Axis


def getAppDistributionOnCells(dcPaths):
    '''
        Aggregate app user & traffic on each cell
        
        Return:
                two dataframes in which row = appID, column = cellID
    '''
    
    dcAppUserNumInCells = {}
    dcAppTrafficInCells = {}
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            
            # update app user
            dcAppUserNumInCurrentCell = dcAppUserNumInCells.get(strKey, None)
            if (None == dcAppUserNumInCurrentCell):
                dcAppUserNumInCurrentCell = {}
                dcAppUserNumInCells[strKey] = dcAppUserNumInCurrentCell
                
            for app in node.m_lsApps:
                updateDictBySum(dcAppUserNumInCurrentCell, app.m_nServiceType, 1)
            
            # update app traffic
            dcAppTrafficInCurrentCell = dcAppTrafficInCells.get(strKey, None)
            if (None == dcAppTrafficInCurrentCell):
                dcAppTrafficInCurrentCell = {}
                dcAppTrafficInCells[strKey] = dcAppTrafficInCurrentCell
                
            updateDictBySumOnAttribute(dcAppTrafficInCurrentCell, node.m_lsApps, "m_nDownBytes")
            
    dfAppUserNumInCells = pd.DataFrame(dcAppUserNumInCells)
    dfAppTrafficInCells = pd.DataFrame(dcAppTrafficInCells)
    
    return dfAppUserNumInCells, dfAppTrafficInCells
    

def getCategoryDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells):
    '''
        aggregate apps into categories
        
        Params:
                dfAppUserNumInCells - dataframe in which row = appID, column = lac-cid
                dfAppTrafficInCells - dataframe in which row = appID, column = lac-cid
    '''
    dcCategoryUser = {}
    dcCategoryTraffic = {}
    
    for tp in app_category.g_dcCategory.items():
        dcCategoryUser[tp[0]] = dfAppUserNumInCells.loc[dfAppUserNumInCells.index.isin(tp[1])].sum(axis=0)
        dcCategoryTraffic[tp[0]] = dfAppTrafficInCells.loc[dfAppTrafficInCells.index.isin(tp[1])].sum(axis=0)
    
    dfCategoryUser = pd.DataFrame(dcCategoryUser)
    dfCategoryTraffic = pd.DataFrame(dcCategoryTraffic)
      
    return dfCategoryUser, dfCategoryTraffic


    
def getTotoalDistributionOnRegions(dfAppUserNumInCells, dfAppTrafficInCells, dfCellType):
    '''
        get user number & total traffic distribution on different types of regions
        
        Params:
                dfAppUserNumInCells - dataframe in which row = appID, column = lac-cid
                dfAppTrafficInCells - dataframe in which row = appID, column = lac-cid
                dfCellType - dataframe in which index = lac-cid, row = cell
        
        Return:
                Tow series likes: {typeName: user_num or traffic_value}
    '''
    dcRegionUserNum = {}
    dcRegionTraffic = {}
    
    sTotalUserInCells = dfAppUserNumInCells.sum(axis=0)
    sTotalTrafficInCells = dfAppTrafficInCells.sum(axis=0)
    
    # user number

    for tpUser in sTotalUserInCells.iteritems():
        strLacCid = tpUser[0]
        nUserNum = tpUser[1]
        nType = 0
        try: 
            nType = int(dfCellType.loc[strLacCid]['typeID'])
        except KeyError as err:
            print err.message
            pass
        updateDictBySum(dcRegionUserNum, region_type.g_dcRegionTypeName.get(nType, 'unknown'), nUserNum)
        
    # traffic
    for tpTraffic in sTotalTrafficInCells.iteritems():
        strLacCid = tpTraffic[0]
        nTraffic = tpTraffic[1]
        nType = 0
        try:
            nType = int(dfCellType.loc[strLacCid]['typeID'])
        except KeyError as err:
            print err.message
            pass
        updateDictBySum(dcRegionTraffic, region_type.g_dcRegionTypeName.get(nType, 'unknown'), nTraffic)
        
    sRegionUserNum = pd.Series(dcRegionUserNum)
    sRegionTraffic = pd.Series(dcRegionTraffic)

    return sRegionUserNum, sRegionTraffic
     
def drawTotalDistributionOnRegions(sRegionUserNum, sRegionTraffic):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    sRegionUserNum.plot(ax=axes[0], kind='bar')
    (sRegionTraffic/sRegionTraffic.sum()).plot(ax=axes[1], kind='bar')
    
    axes[0].set_ylabel('# users')
    axes[1].set_ylabel('traffic volume (%)')
    plt.show()
    
    
def drawTotalDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    # total user number
    sTotalUserNumCDF = dfAppUserNumInCells.sum(axis=0).order(ascending=False).cumsum()/dfAppUserNumInCells.sum(axis=0).sum()
    sTotalUserNumCDF.plot(ax=axes[0], style='-ro', use_index=False)
    axes[0].set_xlabel('cell index sorted by # user')
    axes[0].set_ylabel('# user CDF (%)')
    
    sTotalTrafficCDF = dfAppTrafficInCells.sum(axis=0).order(ascending=False).cumsum()/dfAppTrafficInCells.sum(axis=0).sum()
    sTotalTrafficCDF.plot(ax=axes[1], style='-ro', use_index=False)
    axes[1].set_xlabel('cell index sorted by # user')
    axes[1].set_ylabel('# traffic CDF (%)')
    
    plt.show()
     
def drawCellTypeDistribution(dfCellType):
    ax0 = plt.figure().add_subplot(111)
    sCellNumPerType = dfCellType.groupby('typeID')['lac-cid'].count()
    lsTypeName  = []
    for k in sorted(region_type.g_dcRegionTypeName.keys()):
        name = region_type.g_dcRegionTypeName.get(k, 'unknown')
        lsTypeName.append(name)
    sCellNumPerType = pd.Series(sorted(sCellNumPerType.tolist()), index= lsTypeName)
    sCellNumPerType.plot(ax=ax0, kind='bar')
    plt.show()
    
    

def execute(dcPaths, strCellTypePath):
    # app distribution on cells
    dfAppUserNumInCells, dfAppTrafficInCells = getAppDistributionOnCells(dcPaths)
    
    # category distribution on cells
    drawTotalDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells)
    
    # total user/traffic distribution on regions
    dfCellType = pd.read_csv(strCellTypePath, index_col='lac-cid')
    sRegionUserNum, sRegionTraffic = getTotoalDistributionOnRegions(dfAppUserNumInCells, dfAppTrafficInCells, dfCellType)
    drawTotalDistributionOnRegions(sRegionUserNum, sRegionTraffic)
    

if __name__ == '__main__':
    pass