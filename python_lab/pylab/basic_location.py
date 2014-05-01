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
            nCellID = node.m_nCellID
            
            # update app user
            dcAppUserNumInCurrentCell = dcAppUserNumInCells.get(nCellID, None)
            if (None == dcAppUserNumInCurrentCell):
                dcAppUserNumInCurrentCell = {}
                dcAppUserNumInCells[nCellID] = dcAppUserNumInCurrentCell
                
            for app in node.m_lsApps:
                updateDictBySum(dcAppUserNumInCurrentCell, app.m_nServiceType, 1)
            
            # update app traffic
            dcAppTrafficInCurrentCell = dcAppTrafficInCells.get(nCellID, None)
            if (None == dcAppTrafficInCurrentCell):
                dcAppTrafficInCurrentCell = {}
                dcAppTrafficInCells[nCellID] = dcAppTrafficInCurrentCell
                
            updateDictBySumOnAttribute(dcAppTrafficInCurrentCell, node.m_lsApps, "m_nDownBytes")
            
    dfAppUserNumInCells = pd.DataFrame(dcAppUserNumInCells)
    dfAppTrafficInCells = pd.DataFrame(dcAppTrafficInCells)
    
    return dfAppUserNumInCells, dfAppTrafficInCells
    

def getCategoryDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells):
    '''
        aggregate apps into categories
    '''
    dcCategoryUser = {}
    dcCategoryTraffic = {}
    
    for tp in app_category.g_dcCategory.items():
        dcCategoryUser[tp[0]] = dfAppUserNumInCells.loc[dfAppUserNumInCells.index.isin(tp[1])].sum(axis=0)
        dcCategoryTraffic[tp[0]] = dfAppTrafficInCells.loc[dfAppTrafficInCells.index.isin(tp[1])].sum(axis=0)
    
    dfCategoryUser = pd.DataFrame(dcCategoryUser)
    dfCategoryTraffic = pd.DataFrame(dcCategoryTraffic)
      
    return dfCategoryUser, dfCategoryTraffic

def drawTotalDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    # total user number
    sTotalUserNumCDF = dfAppUserNumInCells.sum(axis=0).order(ascending=False).cumsum()/dfAppUserNumInCells.sum(axis=0).sum()
    sTotalUserNumCDF.plot(ax=axes[0], style='-ro', logx=True)
    axes[0].set_xlabel('cell index sorted by # user')
    axes[0].set_ylabel('# user CDF (%)')
    
    sTotalTrafficCDF = dfAppTrafficInCells.sum(axis=0).order(ascending=False).cumsum()/dfAppTrafficInCells.sum(axis=0).sum()
    sTotalTrafficCDF.plot(ax=axes[1], style='-ro', logx=True)
    axes[1].set_xlabel('cell index sorted by # user')
    axes[1].set_ylabel('# traffic CDF (%)')
    
    plt.show()

def execute(dcPaths):
    print("getAppDistributionOnCells...")
    dfAppUserNumInCells, dfAppTrafficInCells = getAppDistributionOnCells(dcPaths)
    
    print("drawTotalDistributionOnCells..")
    drawTotalDistributionOnCells(dfAppUserNumInCells, dfAppTrafficInCells)
    

if __name__ == '__main__':
    pass