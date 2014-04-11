# -*- coding: utf-8 -*-
'''
Created on 2014年4月10日

@author: jason
'''

from common_function import *

import pandas as pd

DC_ROLE_TRANSPORTATION = dict.fromkeys(range(21, 39))

DC_ROLE_RESIDENCE = dict.fromkeys([46,47,48,49])

DC_ROLE_EDU = dict.fromkeys([52,53,54,55,56,57])

DC_ROLE_WORK = dict.fromkeys([45,59,60,61,62,63,263,265,266,657,658,661,663,664,668,670])
DC_ROLE_WORK.update(dict.fromkeys(range(608,647)))

DC_ROLE_ENTERTAINMENT = dict.fromkeys(range(64,149))
DC_ROLE_ENTERTAINMENT.update(dict.fromkeys(range(169,258)))
DC_ROLE_ENTERTAINMENT.update(dict.fromkeys([268,269,603,604,605,607,648,649,650,651,652,653,655]))

ID_ROLE_UNKNOWN = 0
ID_ROLE_TRANSPORTATION = 1
ID_ROLE_RESIDENCE = 2
ID_ROLE_EDU = 3
ID_ROLE_WORK = 4
ID_ROLE_ENTERTAINMENT = 5

DEFAULT_ROLE_COVERAGE = 2000 # unit = meter

def generatePoiRole(strPOIPath, strOutPath):
    '''
        generate a poi_role_dict as:
        name, addr, citycode,lat,long,pid,pid-parentPID,poiName, roleID
    '''
    dfpoi = pd.read_csv(strPOIPath, index_col='_id')
    lsRoleID = []
    for tp in dfpoi.itertuples():
        nRoleID = ID_ROLE_UNKNOWN
        nPid = int(tp[6])
        if (DC_ROLE_TRANSPORTATION.has_key(nPid) ):
            nRoleID = ID_ROLE_TRANSPORTATION
        elif (DC_ROLE_RESIDENCE.has_key(nPid) ):
            nRoleID = ID_ROLE_RESIDENCE
        elif (DC_ROLE_EDU.has_key(nPid) ):
            nRoleID = ID_ROLE_EDU
        elif (DC_ROLE_WORK.has_key(nPid) ):
            nRoleID = ID_ROLE_WORK
        elif (DC_ROLE_ENTERTAINMENT.has_key(nPid) ):
            nRoleID = ID_ROLE_ENTERTAINMENT
            
        lsRoleID.append(nRoleID)
    
    dfpoi['roleID'] = lsRoleID
    dfpoi.to_csv(strOutPath)      
          
    print("generatePoiRole is finished.")
    
def assignRole2Cell(dfCellLoc, dfPOI):
    '''
        Assign role to each cell according to pois within cell coverage(2km by default)
        
        dfCellLoc: cell_loc_dict, format: lac-cid, lat, long
        dfPOI: poi_role_dict, format: _id,title,address,city,lon,lat,category,categories,catName,roleID
        
        NOTE: 
             This function will chage dfCellLoc inplace
        
    '''
    lsCellRole = []
    for ctp in dfCellLoc.itertuples():
        dCellLat = ctp[1]
        dCellLong = ctp[2]
        if (dCellLat == 0. or dCellLong == 0.):
            lsCellRole.append(ID_ROLE_UNKNOWN)
            continue
        
        # cross over poi list
        dcPoiRoleCount = dict.fromkeys(range(0,6), 0)     
        for ptp in dfPOI.itertuples():
            dPoiLat = ptp[5]
            dPoiLong = ptp[4]
            nPoiRole = ptp[9]
            dDis = calculateDistance(dCellLat, dCellLong, dPoiLat, dPoiLong)
            if(dDis <= DEFAULT_ROLE_COVERAGE):
                dcPoiRoleCount[nPoiRole] += 1
        
        # set cell role
        nCellRole = ID_ROLE_UNKNOWN
        nRoleCount = 0
        for tp in dcPoiRoleCount.items():
            if (tp[1] >nRoleCount ):
                nCellRole = tp[0]
        lsCellRole.append(nCellRole)
    
    dfCellLoc['cellRole'] = lsCellRole

if __name__ == '__main__':
    dfCellLoc = pd.read_csv("d:\\playground\\cell_loc_filled.csv", index_col='lac-cid')
    dfPoi = pd.read_csv("d:\\playground\\weibo_poi_role_gz.txt", index_col='_id')
    assignRole2Cell(dfCellLoc, dfPoi)
    dfCellLoc.to_csv("d:\\playground\\cell_loc_role.txt")