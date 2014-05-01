# -*- coding: utf-8 -*-
'''
Created on 2014年4月10日

@author: jason
'''

from common_function import *

import pandas as pd
import multiprocessing
import math

DC_TYPE_TRANSPORTATION = dict.fromkeys(range(21, 39))

DC_TYPE_RESIDENCE = dict.fromkeys([46,47,48,49])

DC_TYPE_EDU = dict.fromkeys([52,53,54,55,56,57])

DC_TYPE_WORK = dict.fromkeys([45,59,60,61,62,63,263,265,266,657,658,661,663,664,668,670])
DC_TYPE_WORK.update(dict.fromkeys(range(608,647)))

#DC_TYPE_ENTERTAINMENT = dict.fromkeys(range(64,149))
DC_TYPE_ENTERTAINMENT = dict.fromkeys(range(169,258))
DC_TYPE_ENTERTAINMENT.update(dict.fromkeys([268,269,603,604,605,607,648,649,650,651,652,653,655]))

ID_TYPE_UNKNOWN = 0
ID_TYPE_TRANSPORTATION = 1
ID_TYPE_RESIDENCE = 2
ID_TYPE_EDU = 3
ID_TYPE_WORK = 4
ID_TYPE_ENTERTAINMENT = 5

g_dcRegionTypeName = {ID_TYPE_UNKNOWN: "unknown",\
                  ID_TYPE_TRANSPORTATION: "transportation",\
                  ID_TYPE_RESIDENCE: "residence",\
                  ID_TYPE_EDU: "education",\
                  ID_TYPE_WORK: "work",\
                  ID_TYPE_ENTERTAINMENT: "entertainment"}

DEFAULT_REGION_COVERAGE = 2000 # unit = meter

g_dfCellLocType = pd.DataFrame()
g_nCellNum = 0

MAX_PROC_NUM = 30
MAX_CELL_PER_PROC = 1000

ENTERTAIN_POI_WEIGHT = 0.3

def generatePoiType(strPOIPath, strOutPath):
    '''
        generate a poi_type_dict as:
        name, addr, citycode,lat,long,pid,pid-parentPID,poiName, typeID
    '''
    dfpoi = pd.read_csv(strPOIPath, index_col='_id')
    lsTypeID = []
    for tp in dfpoi.itertuples():
        nTypeID = ID_TYPE_UNKNOWN
        nPid = int(tp[6])
        if (DC_TYPE_TRANSPORTATION.has_key(nPid) ):
            nTypeID = ID_TYPE_TRANSPORTATION
        elif (DC_TYPE_RESIDENCE.has_key(nPid) ):
            nTypeID = ID_TYPE_RESIDENCE
        elif (DC_TYPE_EDU.has_key(nPid) ):
            nTypeID = ID_TYPE_EDU
        elif (DC_TYPE_WORK.has_key(nPid) ):
            nTypeID = ID_TYPE_WORK
        elif (DC_TYPE_ENTERTAINMENT.has_key(nPid) ):
            nTypeID = ID_TYPE_ENTERTAINMENT
            
        lsTypeID.append(nTypeID)
    
    dfpoi['typeID'] = lsTypeID
    dfpoi.to_csv(strOutPath)      
    
 
    print("#unknonw POI = %d " % (len(dfpoi[dfpoi['roleID'] == 0])) )
    print("#Transportation POI = %d " % (len(dfpoi[dfpoi['roleID'] == 1])) )
    print("#Residence POI = %d " % (len(dfpoi[dfpoi['roleID'] == 2])) )
    print("#Edu POI = %d " % (len(dfpoi[dfpoi['roleID'] == 3])) )
    print("#Work POI = %d " % (len(dfpoi[dfpoi['roleID'] == 4])) )
    print("#Entertainment POI = %d " % (len(dfpoi[dfpoi['roleID'] == 5])) )

    
def assignType2Cell(dfCellLoc, dfPOI):
    '''
        Assign region type to each cell according to pois within cell coverage(2km by default)
        
        dfCellLoc: cell_loc_dict, format: lac-cid, lat, long
        dfPOI: poi_role_dict, format: _id,title,address,city,lon,lat,category,categories,catName,typeID
        
        NOTE: 
             This function will change dfCellLoc inplace
        
    '''
    lsCellType = []
    for ctp in dfCellLoc.itertuples():
        dCellLat = ctp[1]
        dCellLong = ctp[2]
        if (dCellLat == 0. or dCellLong == 0.):
            lsCellType.append(ID_TYPE_UNKNOWN)
            continue
        
        # cross over poi list
        dcPoiTypeCount = dict.fromkeys(range(0,6), 0)     
        for ptp in dfPOI.itertuples():
            dPoiLat = ptp[5]
            dPoiLong = ptp[4]
            nPoiRole = ptp[9]
            dDis = calculateDistance(dCellLat, dCellLong, dPoiLat, dPoiLong)
            if(dDis <= DEFAULT_REGION_COVERAGE):
                dcPoiTypeCount[nPoiRole] += 1
        
        # set cell role
        nCellType = ID_TYPE_UNKNOWN
        nTypeCount = 0
        dcPoiTypeCount[ID_TYPE_ENTERTAINMENT] = int(dcPoiTypeCount[ID_TYPE_ENTERTAINMENT]*ENTERTAIN_POI_WEIGHT)
        for tp in dcPoiTypeCount.items():
            if (tp[1] >nTypeCount ):
                nCellType = tp[0]
        lsCellType.append(nCellType)
    
    dfCellLoc['typeID'] = lsCellType
    
    return dfCellLoc

def typeAssignmentCallback(rt):
    '''
        merge the assigned cell together
    '''
    global g_dfCellLocType

    # concatenate
    g_dfCellLocType = pd.concat([g_dfCellLocType, rt])
    
    print("==>%d cells have been processed, Progress:%.2f%%" % \
    (len(g_dfCellLocType), len(g_dfCellLocType)*100.0/g_nCellNum) )
    
def assignType2CellInParallel(dfCellLoc, dfPOI, strOutPath):
    '''
        start multiple processes to assign role in parallel
    '''
    global g_nCellNum
    g_nCellNum= len(dfCellLoc)
    
    nCellNum = len(dfCellLoc)
    nPoolSize = MAX_PROC_NUM
    nCellPerProc = min( int(nCellNum/nPoolSize), MAX_CELL_PER_PROC)
    
    pool = multiprocessing.Pool(processes=nPoolSize)
    nStartIndex = 0
    while nStartIndex < nCellNum:
        nEndIndex = min(nStartIndex+nCellPerProc, nCellNum)
        pool.apply_async(assignType2Cell, args=(dfCellLoc[nStartIndex:nEndIndex], dfPOI), callback = typeAssignmentCallback)
        nStartIndex = nEndIndex
    pool.close()
    pool.join()
    
    g_dfCellLocType.to_csv(strOutPath)
    
    

if __name__ == '__main__':
    # setup
    strPoiRolePath = "../../data/weibo_poi_role_gz.txt"
    strPoiPath = "../../data/weibo_poi_gz.txt"
    strCellLocFilled = "../../data/cell_loc_filled.txt"
    strCellLocRole = "../../data/cell_loc_role.txt"

    # generate poi_role_dict
    print("start to generate poi role...")
    generatePoiType(strPoiPath, strPoiRolePath)
    
    #generate cell_loc_role
    print("start to generate poi role...")
    dfCellLoc = pd.read_csv(strCellLocFilled, index_col='lac-cid')
    dfPoi = pd.read_csv(strPoiRolePath, index_col='_id')
    assignType2CellInParallel(dfCellLoc, dfPoi[dfPoi['roleID'] != 0], strCellLocRole)
    print("assignType2CellInParallel is finished.")
