# -*- coding: utf-8 -*-
'''
Created on 2014年4月24日

@author: jason
'''

from common_function import *


import pandas as pd
import matplotlib.pyplot as plt


def getMobility(dcPaths):
    '''
        calculate mobility from raw dcPaths
        
        return
            a tuple of series like: {mobility: #user}
    '''
    dcMobilityCell = {}
    dcMobilitySpeed = {}
    dcMobilityRog = {}
    
    for path in dcPaths.values():
        dcMobilityCell[len(path.m_lsNodes)] = dcMobilityCell.get(len(path.m_lsNodes), 0) + 1
        
        nSpeedLevel = getSpeedLevel(path.m_dMaxSpeed)
        dcMobilitySpeed[nSpeedLevel] = dcMobilitySpeed.get(nSpeedLevel, 0) + 1
        
        nRog = int(calculateRog(path) / 1000.0) # change unit to km, and round up
        dcMobilityRog[nRog] = dcMobilityRog.get(nRog, 0) + 1
        
    sMobilityCell = pd.Series(dcMobilityCell)
    sMobilitySpeed = pd.Series(dcMobilitySpeed)
    sMobilityRog = pd.Series(dcMobilityRog)
    
    return sMobilityCell, sMobilitySpeed, sMobilityRog
    

def drawCDFofMobility(sUserMobilityCell, sUserMobilitySpeed, sUserMobilityRog):
    '''
        draw user CDF of mobility
    '''
    fig, axes = plt.subplots(nrows=1, ncols=3)
    
    # CDF of mobility by cell_num
    sCDFCell = sUserMobilityCell.sort_index().cumsum()*1.0/sUserMobilityCell.sum()
    sCDFCell.plot(ax=axes[0], style='-o', xlim=(1, 50))
    
    # CDF of mobility by rog
    sCDFRog = sUserMobilityRog.sort_index().cumsum()*1.0/sUserMobilityRog.sum()
    sCDFRog.plot(ax=axes[1], style='-o', xlim=(0., 50.))
    
    # CDF of mobility by speed
    sCDFSpeed = sUserMobilitySpeed.sort_index().cumsum()*1.0/sUserMobilitySpeed.sum()
    sCDFSpeed.plot(ax=axes[2], style='-o')
    
    
    # set style
    axes[0].set_xlabel('a. # cells')
    axes[0].set_ylabel('CDF(%)')
    
    axes[1].set_xlabel('b. radius of gyration (km)')
    axes[1].set_ylabel('CDF(%)')
    
    axes[2].set_xlabel('c. speed level')
    axes[2].set_ylabel('CDF(%)')
    
    plt.show()
    
def getRogDistributionOnCellNum(dcPaths):
    '''
        get Rog and cell number for each user
    '''
    lsData = []
    for path in dcPaths.values():
        nCellNum = len(path.m_lsNodes)
        nRog = int(calculateRog(path)/1000.0) # change unit to km, and round up
        lsData.append({'imei':path.m_strIMEI, 'cell_num':nCellNum, 'rog':nRog})
        
    dfRogCellNum = pd.DataFrame(lsData)
    dfRogCellNum.set_index(keys='imei', inplace=True)
    
    return dfRogCellNum

def drawRogDistributionOnCellNum(dfRogCellNum):
    '''
        draw a scatter graph for Rog distribution on cell number
    '''
    plt.scatter(dfRogCellNum['cell_num'], dfRogCellNum['rog'])
    
    plt.xlim((1, 100))
    plt.xlabel('# cells')
    
    plt.ylim((1, 100))
    plt.ylabel('RoG (km)')
    
    plt.show()

def execute(dcPaths):
    sMobilityCell, sMobilitySpeed, sMobilityRog = getMobility(dcPaths)
    drawCDFofMobility(sMobilityCell, sMobilitySpeed, sMobilityRog)

if __name__ == '__main__':
    pass