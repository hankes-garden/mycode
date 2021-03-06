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

DC_TYPE_WORK = dict.fromkeys([45,59,60,61,62,63,258,259,263,265,266, 657,658,661,663,664,668,670])
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

g_dcRegionTypeName = { ID_TYPE_UNKNOWN: "unknown",\
                       ID_TYPE_TRANSPORTATION: "transportation",\
                       ID_TYPE_RESIDENCE: "residence",\
                       ID_TYPE_EDU: "education",\
                       ID_TYPE_WORK: "work",\
                       ID_TYPE_ENTERTAINMENT: "entertainment"}

g_dcRegionWeight = { ID_TYPE_UNKNOWN: 0.001,\
                     ID_TYPE_TRANSPORTATION: 2.0,\
                     ID_TYPE_RESIDENCE: 3.0,\
                     ID_TYPE_EDU: 1.0,\
                     ID_TYPE_WORK: 1.5,\
                     ID_TYPE_ENTERTAINMENT: 0.005 }

DEFAULT_REGION_COVERAGE = 500 # unit = meter

g_dfCellLocType = pd.DataFrame()
g_nCellNum = 0

MAX_PROC_NUM = 30
MAX_CELL_PER_PROC = 1000

ENTERTAIN_POI_WEIGHT = 0.3

g_dcTransportation = {'guangzhou_station': (23.147958, 113.257746), \
                      'guangzhou_east_station': (23.150228, 113.324825), \
                      'guangzhou_south_station': (22.992369, 113.268629), \
                      'baiyun_airport': (23.374559, 113.299875)}

g_dcEdu = {'scut': (23.151658, 113.344774) ,\
           'sysu': (23.092337, 113.293082) ,\
           'scau': (23.159471, 113.351211) ,\
           'university_town_scut': (23.046826, 113.402906), \
           'university_town_SYSU': (23.066826, 113.391941), \
           'university_town_gzu': (23.038918, 113.369332) ,\
           'gdfu': (23.201333, 113.289276) ,\
           'jnu': (23.128214, 113.347565)   }

g_dcWork = {'tianhe_sci_park': (23.124177, 113.372569), \
            'tianhebei': (23.136342, 113.329021), \
            'tianhe_rd': (23.133505, 113.335533), \
            'tianhe_rd_2': (23.134068, 113.328967), \
            'tianhebei_rd': (23.141499, 113.343865), \
            'tianhe_software_park': (23.124167, 113.372563),\
            'cheyueda_automobile_maintenance_center': (23.098685, 113.444092)}

g_dcEntertainment = {'gongyuanqian': (23.125720, 113.264127), \
                     'haixinsha': (23.112475, 113.324092), \
                     'tianhe_city_shopping_center': (23.132360, 113.322699), \
                     'tianhe_tee_fasion_mall': (23.130725, 113.320133), \
                     'beijin_rd': (23.119112, 113.270136), \
                     'grandview_mall':(23.132219, 113.326985) }

def assignType2CellManually(dfCellLoc):
    lsCellType = []
    for ctp in dfCellLoc.itertuples():
        dCellLat = ctp[1]
        dCellLong = ctp[2]
        if (dCellLat == 0. or dCellLong == 0.):
            lsCellType.append(ID_TYPE_UNKNOWN)
            continue
        
        nCellType = ID_TYPE_UNKNOWN
        for loc in g_dcTransportation.values():
            if (calculateDistance(loc[0], loc[1], dCellLat, dCellLong) <= DEFAULT_REGION_COVERAGE ):
                nCellType = ID_TYPE_TRANSPORTATION
                
        for loc in g_dcEdu.values():
            if (calculateDistance(loc[0], loc[1], dCellLat, dCellLong) <= DEFAULT_REGION_COVERAGE ):
                nCellType = ID_TYPE_EDU
                
        for loc in g_dcWork.values():
            if (calculateDistance(loc[0], loc[1], dCellLat, dCellLong) <= DEFAULT_REGION_COVERAGE ):
                nCellType = ID_TYPE_WORK
                
        for loc in g_dcEntertainment.values():
            if (calculateDistance(loc[0], loc[1], dCellLat, dCellLong) <= DEFAULT_REGION_COVERAGE ):
                nCellType = ID_TYPE_ENTERTAINMENT
        
        lsCellType.append(nCellType)
    
    dfCellLoc['typeID'] = lsCellType
    
    return dfCellLoc

def AssignType2Poi(strPOIPath, strOutPath):
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
    
 
    print("#unknonw POI = %d " % (len(dfpoi[dfpoi['typeID'] == 0])) )
    print("#Transportation POI = %d " % (len(dfpoi[dfpoi['typeID'] == 1])) )
    print("#Residence POI = %d " % (len(dfpoi[dfpoi['typeID'] == 2])) )
    print("#Edu POI = %d " % (len(dfpoi[dfpoi['typeID'] == 3])) )
    print("#Work POI = %d " % (len(dfpoi[dfpoi['typeID'] == 4])) )
    print("#Entertainment POI = %d " % (len(dfpoi[dfpoi['typeID'] == 5])) )

    
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
            nPoiType = ptp[9]
            dDis = calculateDistance(dCellLat, dCellLong, dPoiLat, dPoiLong)
            if(dDis <= DEFAULT_REGION_COVERAGE):
                dcPoiTypeCount[nPoiType] += 1
        
        # set cell role
        nCellType = ID_TYPE_UNKNOWN
        nTypeCount = 0
        
        # change scale first
        for k in dcPoiTypeCount.keys():
            dcPoiTypeCount[k] = int(dcPoiTypeCount[k] * g_dcRegionWeight.get(k, 1.0))
        
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
    
def execute():    
     # setup
    strPoiTypePath = "../../data/weibo_poi_gz_type.txt"
    strPoiPath = "../../data/weibo_poi_gz.txt"
    strCellLocFilled = "../../data/cell_loc_filled.txt"
    strCellTypePath = "../../data/cell_loc_type.txt"

    # generate poi_role_dict
    print("start to assign type to POIs...")
    AssignType2Poi(strPoiPath, strPoiTypePath)
    
    #generate cell_loc_role
    print("start to assign type to cells...")
    dfCellLoc = pd.read_csv(strCellLocFilled, index_col='lac-cid')
#     dfPoi = pd.read_csv(strPoiTypePath, index_col='_id')
#     assignType2CellInParallel(dfCellLoc, dfPoi[dfPoi['typeID'] != 0], strCellTypePath)
    dfCellLocType = assignType2CellManually(dfCellLoc)
    dfCellLocType.to_csv(strCellTypePath)
    print("assignType2Cell is finished.")

   
