# -*- coding: utf-8 -*-
'''
Created on 2014年4月3日

@author: y00752450
'''

MIN_VALID_USER_NUM=1000

import numpy as np
import pandas as pd
import matplotlib as mat

from node import *
from common_function import *


g_dcAgg = {}
g_dcAppUserNum = {}

def aggregateData(dcPaths, strAttributeName="m_nDownBytes"):
    '''
        Aggregate data from dcPaths w.r.t given attribute
        return format: row=serviceType, column=cell, value=given_attribute
    '''
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            dcAppsInCell = g_dcAgg.get(strKey)
            if (None == dcAppsInCell): # no corresponding dc yet, then create one
                dcAppsInCell = {}
                g_dcAgg[strKey] = dcAppsInCell
            updateAppDict(dcAppsInCell, node.m_lsApps, strAttributeName)

def getAggregatedData():
    return g_dcAgg            

def updateAppDict(dcApps, lsApps, strAttributeName):
    '''
        update AppDict with given app list
    '''
    if (len(lsApps) == 0 ):
        return
    for app in lsApps:
        oldValue = dcApps.get(app.m_nServiceType)
        if (None == oldValue):
            dcApps[app.m_nServiceType] = app.__dict__.get(strAttributeName)
        else:
            dcApps[app.m_nServiceType] = oldValue + app.__dict__.get(strAttributeName)


def updateDictbySum(dc, key, newValue):
    if key in dc:
        dc[key] += newValue
    else:
        dc[key] = newValue


def AggregateAppUserNum(dcPaths):
    '''
        get user number for each apps
        return a dc likes: {serviceType:user_number}
    '''
    for path in dcPaths.values():
        dcAppsPerUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dcAppsPerUser[app.m_nServiceType] = 1
        for tp in dcAppsPerUser.items():
            updateDictbySum(g_dcAppUserNum, tp[0], tp[1])

def getAggregatedAppUserNum():
    return g_dcAppUserNum


def cleanData(dfAggAll, sAppUserNum):
    '''
        clean data based on some criteria
        1. top 100 app based on #user
    '''
    sSelectedApps = sAppUserNum.order(ascending=False)[:100]
    dfAggAllCleaned = dfAggAll.loc[sSelectedApps.index]
    return dfAggAllCleaned

import sys
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        raise StandardError("Usage: data_loader.py cell_loc_dict_path serialized_path_1, [serialized_path_2]")
    
    strCellLocPath = sys.argv[1]
    lsSerPath = sys.argv[2:len(sys.argv)]
    
    for sp in lsSerPath: 
        print("Start to deserialize from %s" % sp) 
        dcPaths = deserializeFromFile(sp)
         
        print("Start to aggregate data by m_nDownBytes...")
        aggregateData(dcPaths)
        
        print("Start to aggregate user number...")
        AggregateAppUserNum(dcPaths)
    
    dcAgg = getAggregatedData()
    dcAggregatedAppUserNum = getAggregatedAppUserNum()
    print("Aggregation is finished")  
    del dcPaths
     
    print("Start to construct cell-location dict...")
    dcCellLocDict = constructCellLocDict(strCellLocPath)
    
    dfAgg = pd.DataFrame(dcAgg)
    sAppUserNum = pd.Series(dcAggregatedAppUserNum)
    
    del dcAgg
    del dcAggregatedAppUserNum
    
    
    print("Start to clean data...")
    dfAggCleaned = cleanData(dfAgg, sAppUserNum)
    del dfAgg
    
    print("data_loader is ready!")
    
    
    