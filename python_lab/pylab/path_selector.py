# -*- coding: utf-8 -*-
'''
This module select path of subscribers based on some conditions 

@author: jason
'''

import time
import copy

import pandas as pd

from common_function import calculateRog

ID_NETWORK_3G = 1 
ID_NETWORK_2G = 2

def selectPathByMobility(dcTotalPaths, nTop, strMobilityIndicator='cell_num'):
    '''
        find paths of heavy mobile users and normal user
        
        return:
                dfUserMobility - a dataframe like: {imei: {'up_bytes', 'down_bytes'}}
                dcHeavyUserPaths - a dict of paths for top users
                
    '''
    
    lsData = []
    for path in dcTotalPaths.values():
        nCellNum = len(path.m_lsNodes)
        nRog = int(calculateRog(path) / 1000.0) # change unit to km, and round up
        lsData.append({'imei': path.m_strIMEI, 'cell_num': nCellNum, 'rog': nRog})

    dfUserMobility = pd.DataFrame(lsData)
    dfUserMobility.set_index('imei', inplace=True)
    
    # find top users by mobility
    dfUserMobility.sort(column = strMobilityIndicator, ascending=False, inplace=True)
    
    lsHeavyUsers = dfUserMobility.iloc[:nTop].index
    dcHeavyUserPaths = {}
    dcNormalUserPaths = {}
    for tp in dcTotalPaths.items():
        if tp[0] in lsHeavyUsers:
            dcHeavyUserPaths[tp[0]] = tp[1]
        else:
            dcNormalUserPaths[tp[0]] = tp[1]
    
    
    return dfUserMobility, dcHeavyUserPaths, dcNormalUserPaths

def selectPathByTraffic(dcTotalPaths, nTop):
    '''
        find paths for heavy users
        
        return:
                dfUserTraffic - a dataframe like: {imei: {'up_bytes', 'down_bytes'}}
                dcHeavyUserPaths - a dict of paths for top users
                
    '''
    
    lsData = []
    for path in dcTotalPaths.values():
        nUpBytes = 0
        nDownBytes = 0
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                nUpBytes += app.m_nUpBytes
                nDownBytes += app.m_nDownBytes
        lsData.append({'imei': path.m_strIMEI, 'up_bytes': nUpBytes, 'down_bytes': nDownBytes})

    dfUserTraffic = pd.DataFrame(lsData)
    dfUserTraffic.set_index('imei', inplace=True)
    
    # find top users by traffic
    dfUserTraffic.sort(column = 'down_bytes', ascending=False, inplace=True)
    
    lsHeavyUsers = dfUserTraffic.iloc[:nTop].index
    dcHeavyUserPaths = {}
    dcNormalUserPaths = {}
    for tp in dcTotalPaths.items():
        if tp[0] in lsHeavyUsers:
            dcHeavyUserPaths[tp[0]] = tp[1]
        else:
            dcNormalUserPaths[tp[0]] = tp[1]
    
    
    return dfUserTraffic, dcHeavyUserPaths, dcNormalUserPaths
    


def selectPathByNetwork(dcTotalPaths):
    '''
        get paths of 2G and 3G
    '''
    dc2G = {}
    dc3G = {}
    
    b3G = False
    for tp in dcTotalPaths.items():
        key = tp[0]
        path = tp[1]
        for node in path.m_lsNodes:
            if (node.m_nRat == ID_NETWORK_3G) : # if this user ever uses 3G in one node, then he/she is 3G user
                b3G = True
                break
        
        if (b3G):
            dc3G[key] = path
        else:
            dc2G[key] = path
            
    return dc2G, dc3G
    

def selectPathByTime(dcPaths, strStartTime, strEndTime):
    '''
    Truncate path by time, time format: %Y-%m-%d %H:%M:%S, e.g., 2014-12-01 16:07:06
    '''
    strFormat = "%Y-%m-%d %H:%M:%S"
    nStart = 0
    nEnd = 0
    if(strStartTime != ''):
        t = time.strptime(strStartTime, strFormat)
        nStart = time.mktime(t)
        
    if(strEndTime != ''):
        t = time.strptime(strEndTime, strFormat)
        nEnd = time.mktime(t)
    
    
    dcSelectedPaths = {}
    for tp in dcPaths.items():
        key = tp[0]
        path = tp[1]
        
        lsNewNodes = []
        for node in path.m_lsNodes:
            if (
                (time.mktime(node.m_firstTime) >= nStart)    \
                and (time.mktime(node.m_firstTime) <= nEnd) \
                and (time.mktime(node.m_endTime) >= nStart)   \
                and (time.mktime(node.m_endTime) <= nEnd)   \
                ):
                lsNewNodes.append(node)
        
        if(len(lsNewNodes) != 0):
            selectedPath = copy.deepcopy(path) #deep copy
            selectedPath.m_lsNodes = lsNewNodes
            dcSelectedPaths[key] = selectedPath
    
    return dcSelectedPaths


if __name__ == '__main__':
    pass