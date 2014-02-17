# -*- coding: utf-8 -*-
'''
Created on 2014年2月16日

@author: lyangab
'''

from app_state import *
from common_function import *

import sys


def measure_app_mobility(lsResult):
    '''Measure application mobility'''
    dcUserMobility = dict()
    dcCurAppDict = 0
    curAppState = 0
    strLastIMEI = 0
    
    for path in lsResult:
        nCurPathLen = len(path)
        print("Path len:%d, Imei:%s" % (nCurPathLen, path[0].m_strIMEI) )
        
        if(nCurPathLen not in dcUserMobility):
            dcCurAppDict = dict()
            dcUserMobility[nCurPathLen] = dcCurAppDict
        else:
            dcCurAppDict = dcUserMobility[nCurPathLen]
            
        for node in path:
            print("--CellID:%d, app list length:%d " % (node.m_nCellID, len(node.m_lsApps) ) )
            
            for app in node.m_lsApps:
                print("----ServiceType:%d" % (app.m_nServiceType) )
                
                if(app.m_nServiceType not in dcCurAppDict):
                    curAppState = CAppState(app.m_nServiceType, app.m_nServiceGroup)
                    dcCurAppDict[app.m_nServiceType] = curAppState
                else:
                    curAppState = dcCurAppDict[app.m_nServiceType]
                
                if(strLastIMEI != node.strIMEI): # count if it's a new user
                    curAppState.m_nUserNum += 1
                    strLastIMEI = node.strIMEI
                
                curAppState.m_nCellNum += 1
                
#               uplink_bytes
                curAppState.m_nAvgUpBytes += app.m_nUpBytes
                curAppState.m_nMaxUpBytes = max(curAppState.m_nMaxUpBytes, app.m_nUpBytes)
                curAppState.m_nMinUpBytes = min(curAppState.m_nMinUpBytes, app.m_nUpBytes) 
                
#               uplink_speed
                curAppState.m_dAvgUpSpeed += app.m_dUpSpeed
                curAppState.m_dMaxUpSpeed = max(curAppState.m_dMaxUpSpeed, app.m_dUpSpeed)
                curAppState.m_dMinUpSpeed = min(curAppState.m_dMinUpSpeed, app.m_dUpSpeed) 
                
#               downlink_bytes
                curAppState.m_nAvgDownBytes += app.m_nDownBytes
                curAppState.m_nMaxDownBytes = max(curAppState.m_nMaxDownBytes, app.m_nDownBytes)
                curAppState.m_nMinDownBytes = min(curAppState.m_nMinDownBytes, app.m_nDownBytes) 
                
#               downlink_speed
                curAppState.m_dAvgDonwSpeed += app.m_dDownSpeed
                curAppState.m_dMaxDownSpeed = max(curAppState.m_dMaxDownSpeed, app.m_dDownSpeed)
                curAppState.m_dMinDownSpeed = min(curAppState.m_dMinDownSpeed, app.m_dDownSpeed)
                
#                 #update app_dict_per_moblity
#                 dcCurAppDict[app.m_nServiceType] = curAppState
#             
#         #update user_mobility_dict
#         dcUserMobility[nCurPathLen] = dcCurAppDict

    # calculate average
    for appDict in dcUserMobility.values():
        for state in appDict.values(): # NOTE: here, the divisor is different!
            state.m_nAvgUpBytes = state.m_nAvgUpBytes/state.m_nUserNum
            state.m_dAvgUpSpeed = state.m_dAvgUpSpeed/state.m_nCellNum
            state.m_nAvgDownBytes = state.m_nAvgDownBytes/state.m_nUserNum
            state.m_dAvgDownSpeed = state.m_dAvgDownSpeed/state.m_nCellNum
            
    return dcUserMobility

                    

if __name__ == '__main__':
    lsResult = 0
    lsResult = deserializeFromFile(sys.argv[1])
    measure_app_mobility(lsResult)

