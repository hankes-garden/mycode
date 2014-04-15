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


def aggregateData(dcPaths, strAttributeName="m_nDownBytes"):
    '''
        Aggregate data from dcPaths w.r.t given attribute
        return format: row=serviceType, column=cell, value=given_attribute
    '''
    dcAggregated = {}
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            dcAppsInCell = dcAggregated.get(strKey)
            if (None == dcAppsInCell): # no corresponding dc yet, then create one
                dcAppsInCell = {}
                dcAggregated[strKey] = dcAppsInCell
            updateAppDict(dcAppsInCell, node.m_lsApps, strAttributeName)
    return dcAggregated
            

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


def getAppUserNum(dcPaths):
    '''
        get user number for each apps
        return a dc likes: {serviceType:user_number}
    '''
    dcAppUserNum = {}
    for path in dcPaths.values():
        dcAppsPerUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dcAppsPerUser[app.m_nServiceType] = 1
                
        for tp in dcAppsPerUser.items():
            updateDictbySum(dcAppUserNum, tp[0], tp[1])
    return dcAppUserNum

def cleanData(dcAggAll, dcUserNum):
    '''
        clean data based on some criteria
        1. user_number < minimal requirement
    '''
    for tp in dcUserNum.items():
        if tp[1] < MIN_VALID_USER_NUM:
            nUserNum = dcAggAll.pop(tp[0], 0)
            print("=>pop: serviceType=%d, user_num=%d" % (tp[0], tp[1]) )
            
    

import sys
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        raise StandardError("Usage: data_loader.py serialized_path cell_loc_dict_path")
     
    print("Start to deserialize from file...") 
    dcPaths = deserializeFromFile(sys.argv[1])
     
    print("Start to aggregate data by m_nDownBytes...")
    dcAggregated = aggregateData(dcPaths)
    
    print("Start to get user number...")
    dcAppUserNum = getAppUserNum(dcPaths)
     
    print("Start to clean data...")
    cleanData(dcAggregated, dcAppUserNum)
    
    print("Start to construct cell-location dict...")
    dcCellLocDict = constructCellLocDict(sys.argv[2])
    
    dfAgg = pd.DataFrame(dcAggregated)
    print("data_loader is ready!")
    
    
    