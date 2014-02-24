# -*- coding: utf-8 -*-
'''
Created on 2014年2月16日

@author: lyangab
'''

from app_state import *
from common_function import *

import sys


def measureAppMobility(lsResult):
    '''
        Measure application mobility
    '''
    dcUserMobility = dict()
    dcCurAppDict = 0
    curAppState = 0
    
    for path in lsResult:
        nCurPathLen = len(path)
        if (nCurPathLen == 0): # skip those empty paths
            continue
        
        if(nCurPathLen not in dcUserMobility):
            dcCurAppDict = dict()
            dcUserMobility[nCurPathLen] = dcCurAppDict
        else:
            dcCurAppDict = dcUserMobility[nCurPathLen]
            
        for node in path:
            for app in node.m_lsApps:
                if(app.m_nServiceType not in dcCurAppDict):
                    curAppState = CAppState(app.m_nServiceType, app.m_nServiceGroup)
                    dcCurAppDict[app.m_nServiceType] = curAppState
                else:
                    curAppState = dcCurAppDict[app.m_nServiceType]
                
                # update AppState
                if(curAppState.m_strLastImei != node.m_strIMEI): # count if it's a new user
                    curAppState.m_nUserNum += 1
                    curAppState.m_strLastImei = node.m_strIMEI
                
                curAppState.m_nAvgCellNum += 1
                
                # uplink_bytes
                curAppState.m_nTotalUpBytes += app.m_nUpBytes
                curAppState.m_nMaxUpBytes = max(curAppState.m_nMaxUpBytes, app.m_nUpBytes)
                curAppState.m_nMinUpBytes = min(curAppState.m_nMinUpBytes, app.m_nUpBytes) 
                
                # uplink_speed
                curAppState.m_dAvgUpSpeed += app.m_dUpSpeed
                curAppState.m_dMaxUpSpeed = max(curAppState.m_dMaxUpSpeed, app.m_dUpSpeed)
                curAppState.m_dMinUpSpeed = min(curAppState.m_dMinUpSpeed, app.m_dUpSpeed) 
                
                # downlink_bytes
                curAppState.m_nTotalDownBytes += app.m_nDownBytes
                curAppState.m_nMaxDownBytes = max(curAppState.m_nMaxDownBytes, app.m_nDownBytes)
                curAppState.m_nMinDownBytes = min(curAppState.m_nMinDownBytes, app.m_nDownBytes) 
                
                # downlink_speed
                curAppState.m_dAvgDownSpeed += app.m_dDownSpeed
                curAppState.m_dMaxDownSpeed = max(curAppState.m_dMaxDownSpeed, app.m_dDownSpeed)
                curAppState.m_dMinDownSpeed = min(curAppState.m_dMinDownSpeed, app.m_dDownSpeed)


    # calculate average
    for appDict in dcUserMobility.values():
        for state in appDict.values(): # NOTE: here, the divisor is different!
            state.m_nAvgCellNum = state.m_nAvgCellNum/state.m_nUserNum
            state.m_nAvgUpBytes = state.m_nTotalUpBytes/state.m_nUserNum
            state.m_dAvgUpSpeed = state.m_dAvgUpSpeed/state.m_nAvgCellNum
            state.m_nAvgDownBytes = state.m_nTotalDownBytes/state.m_nUserNum
            state.m_dAvgDownSpeed = state.m_dAvgDownSpeed/state.m_nAvgCellNum
            
    return dcUserMobility

                    
def conductAppMobilityMeasurement(strInPath, strOutPath):
    '''
        Output format:
        Mobility, ServiceType, ServiceGroup, UserNum, AvgCellNum, TotalUpBytes, AvgUpBytes, 
        MaxUpBytes, MinUpBytes, AvgUpSpeed, MaxUpSpeed, MinUpSpeed, TotalDownBytes, 
        AvgDownBytes, MaxDownBytes, MinDownBytes, AvgDownSpeed, MaxDownSpeed, MinDownSpeed
    '''
    lsResult = deserializeFromFile(strInPath)
    dcUserMobility = measureAppMobility(lsResult)
    strResult = ""
    for tp in dcUserMobility.items():
        for app in tp[1].values():
            strResult += "%d,%s\n" % (tp[0], app.toString() )
    write2File(strResult, strOutPath)

if __name__ == '__main__':
    conductAppMobilityMeasurement("D:\yanglin\playground\serPath_71906_export-userservice-2013100311_export-userservice-2013100315.txt",\
                                  "D:\\yanglin\\playground\\appmob_71906_export-userservice-2013100311_export-userservice-2013100315.txt")

