# -*- coding: utf-8 -*-
'''
Created on 2014年4月3日

@author: y00752450
'''

MIN_VALID_USER_NUM=1000

import numpy as np
import pandas as pd
import matplotlib as mat
import gc

from node import *
from common_function import *


def aggregateDataIncrementally(dcPaths, dcAgg, strAttributeName="m_nDownBytes"):
    '''
        Aggregate data from dcPaths w.r.t given attribute incrementally
        Params:
                dcPath - piece of dcPath
                dcAgg - the dcAgg which stored previous aggregated data
                strAttributeName - the attribute name
        Return:
                format: row=serviceType, column=cell, value=given_attribute
    '''
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            dcAppsInCell = dcAgg.get(strKey)
            if (None == dcAppsInCell): # no corresponding dc yet, then create one
                dcAppsInCell = {}
                dcAgg[strKey] = dcAppsInCell
            updateDictBySumOnAttribute(dcAppsInCell, node.m_lsApps, strAttributeName)
   




def AggregateAppUserNumIncrementally(dcPaths, dcAppUserNum):
    '''
        Aggregate App User Num Incrementally
        
        Params:
                dcPaths - piece of dcPaths
                dcAppUserNum - The dict which stores previous aggregated App user number, 
                               format: {serviceType:user_number}
    '''
    for path in dcPaths.values():
        dcAppsPerUser = {}
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                dcAppsPerUser[app.m_nServiceType] = 1
        for tp in dcAppsPerUser.items():
            updateDictBySum(dcAppUserNum, tp[0], tp[1])


def cleanData(dfAggAll, sAppUserNum, nTopApp):
    '''
        Clean data based on some criteria:
            1. all user-intended apps(network_related_apps are excluded)
            2. top 100 app based on #user
    '''
    lsLabel = []
    for lb in dfAggAll.index:
        nLb = int(lb)
        if(nLb>=17000 and nLb<=21000): #exclude all network_related_apps
            continue
        lsLabel.append(lb)
    
    sSelectedApps = sAppUserNum.loc[lsLabel].order(ascending=False)[:nTopApp]
    dfAggAllCleaned = dfAggAll.loc[sSelectedApps.index]
    return dfAggAllCleaned

def execute(strSerPathDir, strCellLocPath, bRaw, nTopApp = 100):
    '''
        return a tuple of three data:
        tp[0] - dcTotalPaths
        tp[1] - sAppUserNum
        tp[2] - cleaned data
        tp[3] - dcCellLoc
    '''
    
    lsSerPath = []
    for (dirpath, dirnames, filenames) in os.walk(strSerPathDir):
        for fn in sorted(filenames):
            lsSerPath.append(dirpath+fn)
    
    dcTotoalPaths = {}
    dcAggData = {}
    dcAggAppUserNum = {}
    for sp in lsSerPath: 
        print("Start to deserialize from %s" % sp) 
        dcPaths = deserializeFromFile(sp)
         
        print("Start to aggregate data by m_nDownBytes...")
        aggregateDataIncrementally(dcPaths, dcAggData)
        
        print("Start to aggregate user number...")
        AggregateAppUserNumIncrementally(dcPaths, dcAggAppUserNum)
        
        if(True == bRaw):
            dcTotoalPaths.update(dcPaths)
        
        del dcPaths
        gc.collect()
    print("Data Aggregation is finished")  
    
    dfAgg = pd.DataFrame(dcAggData)
    sAppUserNum = pd.Series(dcAggAppUserNum)
    del dcAggData
    del dcAggAppUserNum
    
    print("Start to clean data...")
    dfAggCleaned = cleanData(dfAgg, sAppUserNum, nTopApp)
    del dfAgg
    
    print("Start to construct cell-location dict...")
    dcCellLocDict = constructCellLocDict(strCellLocPath)
    
    # release memory      
    gc.collect()
    
    return dcTotoalPaths, sAppUserNum, dfAggCleaned, dcCellLocDict

import sys
if __name__ == '__main__':
    '''
        sys.argv[1] - path of cell_loc_dict
        sys.argv[2] - store raw dcPaths in memory? 1 means yes and 0 means no
        sys.argv[3] - dir of serialized paths
        
        return nothing, but all loaded data are store in context variables
    '''
    if (len(sys.argv) != 4):
        raise MyError("Usage: data_loader.py cell_loc_dict_path output_dir serialized_path_1, [serialized_path_2]")
    
    strCellLocPath = sys.argv[1]
    bRaw = True if sys.argv[2] == '1' else False
    strSerPathDir = sys.argv[3]
    
    execute(strCellLocPath, bRaw, strSerPathDir)
    
    
    
    
    
    