# -*- coding: utf-8 -*-
'''
Created on 2014年4月24日

@author: jason
'''

from common_function import *

import pandas as pd
import matplotlib.pyplot as plt

def getMobilityDistribution(dcPaths):
    '''
        This function computes subscribers' mobility from raw dcPaths
        
        Param:
                dcPath - {strIMEI: CPath instance, ...}
        return:
                a tuple of series like: {mobility: #user}
                
        Note:
                When computing the rog, some users' paths are not counted as
                most of its node locations are missing, but when computing #cell,
                all the paths are counted, Therefore, the total user number counted
                from rog is smaller than total user number counted from #cell. Whenever
                using this result, be aware of this difference!
    '''
    dcUserNumPerCell = {}
    dcUserNumPerSpeed = {}
    dcUserNumPerRog = {}
    
    nUnconvincingPathCount = 0
    for path in dcPaths.values():
        
        #=======================================================================
        # mobility in #cell
        #=======================================================================
        cellNum, dConfidenceRatio = computeSubscriberMobility(path, g_strMobilityInCell)
        if (dConfidenceRatio < g_dMinConfidenceRatio):
            continue # mobility information is not convincing, skip it
        dcUserNumPerCell[cellNum] = dcUserNumPerCell.get(cellNum, 0) + 1
        
        #=======================================================================
        # mobility in speed
        #=======================================================================
        nSpeedLevel = getSpeedLevel(path.m_dMaxSpeed)
        dcUserNumPerSpeed[nSpeedLevel] = dcUserNumPerSpeed.get(nSpeedLevel, 0) + 1
        
        #=======================================================================
        # mobility in rog
        #=======================================================================
        rog, dConfidenceRatio = computeSubscriberMobility(path, g_strMobilityInRog)
        if (dConfidenceRatio < g_dMinConfidenceRatio):
            nUnconvincingPathCount += 1
            continue # mobility information is not convincing, skip it
        dcUserNumPerRog[rog] = dcUserNumPerRog.get(rog, 0) + 1
        
    print("%s of %s paths are unconvincing" % (nUnconvincingPathCount, len(dcPaths) ) )
    sUserNumPerCell = pd.Series(dcUserNumPerCell)
    sUserNumPerSpeed = pd.Series(dcUserNumPerSpeed)
    sUserNumPerRog = pd.Series(dcUserNumPerRog)
    
    return sUserNumPerCell, sUserNumPerSpeed, sUserNumPerRog
    

def drawCDFofMobility(sUserMobilityCell, sUserMobilitySpeed, sUserMobilityRog, \
                      axes=None, strLable=None, strStyle= '-', bDraw=True):
    '''
        draw user CDF of mobility
    '''
    if (None == axes):
        fig, axes = plt.subplots(nrows=1, ncols=2)
    
    # CDF of mobility by cell_num
    sCDFCell = sUserMobilityCell.sort_index().cumsum()*1.0/sUserMobilityCell.sum()
    sCDFCell.plot(ax=axes[0], style= strStyle, xlim=(1, 50), ylim=(0.3, 1.0), label=strLable)
    
    # CDF of mobility by rog
    sCDFRog = sUserMobilityRog.sort_index().cumsum()*1.0/sUserMobilityRog.sum()
    sCDFRog.plot(ax=axes[1], style= strStyle, xlim=(0., 50.), ylim=(0.3, 1.0), label=strLable)
    
#     # CDF of mobility by speed
#     sCDFSpeed = sUserMobilitySpeed.sort_index().cumsum()*1.0/sUserMobilitySpeed.sum()
#     sCDFSpeed.plot(ax=axes[2], style= strStyle, label=strLable)
    
    
    # set style
    axes[0].set_xlabel('# cells')
    axes[0].set_ylabel('CDF(%)')
    
    axes[1].set_xlabel('radius of gyration (km)')
    axes[1].set_ylabel('CDF(%)')
#     
#     axes[2].set_xlabel('speed level')
#     axes[2].set_ylabel('CDF(%)')
    
    if (bDraw):
        if (strLable != None):
            for ax in axes:
                ax.legend(loc='lower right')
        plt.show()
    
    
def getMobility(dcPaths):
    '''
        get Rog and cell number for each user
        
        return:
                a dataframe: row = imei, columns = cell_num, rog, speed
    '''
    lsData = []
    for path in dcPaths.values():
        nCellNum = len(path.m_lsNodes)
        nRog = int(calculateRog(path)/1000.0) # change unit to km, and round up
        dSpeed = path.m_dMaxSpeed
        lsData.append({'imei':path.m_strIMEI, 'cell_num':nCellNum, 'rog':nRog, 'speed':dSpeed})
        
    dfMobility = pd.DataFrame(lsData)
    dfMobility.set_index(keys='imei', inplace=True)
    
    return dfMobility

def drawRogDistributionOnCellNum(dfMobility):
    '''
        draw a scatter graph for Rog distribution on cell number
        
        param:
                dfMobility - a dataframe: row = imei, columns = cell_num, rog, speed
    '''
    plt.scatter(dfMobility['cell_num'], dfMobility['rog'])
    
    plt.xlim((1, 100))
    plt.xlabel('# cells')
    
    plt.ylim((1, 100))
    plt.ylabel('RoG (km)')
    
    plt.show()

def execute(dcPaths):
    sUserNumPerCell, sUserNumPerSpeed, sUserNumPerRog = getMobilityDistribution(dcPaths)
    drawCDFofMobility(sUserNumPerCell, sUserNumPerSpeed, sUserNumPerRog, bDraw=True)
    

if __name__ == '__main__':
    pass