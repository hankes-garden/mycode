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


def aggregateDataInAppCellIncrementally(dcPaths, dcAgg, strAttributeName="m_nDownBytes"):
    '''
        This function aggregate all subscribers' volume of given attribute in 
        serviceType-cell-format incrementally
        
        Params:
                dcPath - piece of dcPath
                dcAgg - the dcAgg which stored previous aggregated data, 
                        format: row=serviceType, column=cell, value=given_attribute
                strAttributeName - the attribute name
                
    '''
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            dcAppsInCell = dcAgg.get(strKey)
            if (None == dcAppsInCell): # no corresponding dc yet, then create one
                dcAppsInCell = {}
                dcAgg[strKey] = dcAppsInCell
            updateDictBySumOnAttribute(dcAppsInCell, node.m_lsApps, strAttributeName)

def aggregateAppUserNumIncrementally(dcPaths, dcAppUserNum):
    '''
        Aggregate App User Num in format of app-cell format incrementally
        
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


def cleanData(dfAggData, sAppUserNum, nTopApp):
    '''
        Clean data based on some criteria:
            1. all user-intended apps(network_related_apps are excluded)
            2. top n app based on #user
    '''
    lsLabel = []
    for lb in dfAggData.index:
        nLb = int(lb)
        if(nLb>=17000 and nLb<=21000): #exclude all network_related_apps
            continue
        lsLabel.append(lb)
    
    sSelectedApps = sAppUserNum.loc[lsLabel].order(ascending=False)[:nTopApp]
    dfAggAllCleaned = dfAggData.loc[sSelectedApps.index]
    return dfAggAllCleaned, sSelectedApps

def execute(strSerPathDir, strCellLocPath, bRaw, nTopApp = 100, bClean=True):
    '''
        This function aggregate user number and downlink traffic of each app
        in the format of app-cell format, and then filter out the unqualified apps
        
        param:
                strSerPathDir     - path of all serialized roaming path
                strCellLocPath    - path of cell - location mapping file
                bRaw              - if True, the dcTotalPaths in return params contains roaming path of all users
                nTopApp           - number of top apps to analyze
                bClean            - True for cleaning unqualified apps
        return a tuple of three data:
                tp[0] - dcTotalPaths, if bRaw is true, then this dict contains roaming paths of all users
                tp[1] - sCleanedUserNum, User number statistics
                tp[2] - dfCleanedDLTraffic, pd.DataFrame of cleaned downlink traffic volume
                tp[3] - dcCellLocDict, dict of cell-location mapping
    '''
    
    lsSerPath = []
    for (dirpath, dirnames, filenames) in os.walk(strSerPathDir):
        for fn in sorted(filenames):
            lsSerPath.append(dirpath+fn)
    
    dcTotalPaths = {}
    dcAggDLTraffic = {}
    dcAggAppUserNum = {}
    for sp in lsSerPath: 
        print("Start to deserialize from %s" % sp) 
        dcPaths = deserializeFromFile(sp)
         
        print("Start to aggregate data by m_nDownBytes...")
        aggregateDataInAppCellIncrementally(dcPaths, dcAggDLTraffic)
        
        print("Start to aggregate user number...")
        aggregateAppUserNumIncrementally(dcPaths, dcAggAppUserNum)
        
        if(True == bRaw):
            dcTotalPaths.update(dcPaths)
        
        del dcPaths
        gc.collect()
    print("Data Aggregation is finished")  
    
    dfAggDLTraffic = pd.DataFrame(dcAggDLTraffic)
    sAppUserNum = pd.Series(dcAggAppUserNum)
    del dcAggDLTraffic
    del dcAggAppUserNum
    
    if(bClean):
        print("Start to clean data...")
        dfCleanedDLTraffic, sCleanedUserNum = cleanData(dfAggDLTraffic, sAppUserNum, nTopApp)
    else:
        dfCleanedDLTraffic = dfAggDLTraffic
        sCleanedUserNum = sAppUserNum
    
    print("Start to construct cell-location dict...")
    dcCellLocDict = constructCellLocDict(strCellLocPath)
    
    # release memory      
    gc.collect()
    
    return dcTotalPaths, sCleanedUserNum, dfCleanedDLTraffic, dcCellLocDict

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
    
    
    
    
    
    