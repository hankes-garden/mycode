# -*- coding: utf-8 -*-
'''
Created on 2014年2月16日

@author: lyangab
'''

from app_state import *
from common_function import *

import sys
import math

def getSpeedLevel(dSpeed):
    
    # change to km/h, and divide into slots
    sp = (dSpeed*60.0*60.0/1000.0)/10
    
    nLevel = 0
    if (0.0<sp<=10.0):
        nLevel = 1
    if (10.0<sp<=20.0):
        nLevel = 2
    if (20.0<sp<=30.0):
        nLevel = 3
    if (30.0<sp<=40.0):
        nLevel = 4
    if (40.0<sp<=50.0):
        nLevel = 5
    if (50.0<sp<=60.0):
        nLevel = 6
    if (60.0<sp<=70.0):
        nLevel = 7
    if (70.0<sp<=80.0):
        nLevel = 8
    if (80.0<sp<=90.0):
        nLevel = 9
    if (sp>90.0):
        nLevel = 10
        
    return nLevel


def measureAppMobility(dcPaths, bySpeed=False):
    '''
        Measure application mobility
    '''
    dcUserMobility = {}
    dcCurAppDict = 0
    curAppState = 0
    
    for path in dcPaths.values():
        if (len(path.m_lsNodes) == 0): # skip those empty paths
            continue
        
        nCurPathIndex = getSpeedLevel(path.m_dAvgSpeed) if bySpeed else len(path.m_lsNodes)
        
        if(nCurPathIndex not in dcUserMobility):
            dcCurAppDict = dict()
            dcUserMobility[nCurPathIndex] = dcCurAppDict
        else:
            dcCurAppDict = dcUserMobility[nCurPathIndex]
            
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                if(app.m_nServiceType not in dcCurAppDict):
                    curAppState = CAppState(app.m_nServiceType, app.m_nServiceGroup, app.m_nUserPort,\
                                            app.m_nDstPort, app.m_nProtocol)
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

                    
def conductAppMobilityMeasurement(strInPath, strOutPath, dcPaths = None):
    '''
        Output format:
        Mobility, 
        ServiceType, ServiceGroup, UserNum, AvgCellNum, TotalUpBytes, 
        AvgUpBytes, MaxUpBytes, MinUpBytes, AvgUpSpeed, MaxUpSpeed, 
        MinUpSpeed, TotalDownBytes, AvgDownBytes, MaxDownBytes, 
        MinDownBytes, AvgDownSpeed, MaxDownSpeed, MinDownSpeed, 
        Protocol, UserPort, DstPort
    '''
    if (dcPaths == None):
        print("Start to deserialize path...")
        dcPaths = deserializeFromFile(strInPath)

    # based on #cell_visited
    print("Start to measure application mobility based on vistied cell...")
    dcCellMobility = measureAppMobility(dcPaths, False)
    strCellResult = ""
    for tp in dcCellMobility.items():
        for app in tp[1].values():
            strCellResult += "%d,%s\n" % (tp[0], app.toString() )
    write2File(strCellResult, strOutPath+"_cell.txt")

    # based on moving speed
    print("Start to measure application mobility based on speed...")
    dcSpeedMobility = measureAppMobility(dcPaths, True)
    strSpeedResult = ""
    for tp in dcSpeedMobility.items():
        for app in tp[1].values():
            strSpeedResult += "%d,%s\n" % (tp[0], app.toString() )
    write2File(strSpeedResult, strOutPath+"_speed.txt")
    
    print("Application mobility is finished!")

import sys
if __name__ == '__main__':
    print("====Start application mobility measurement...====")
    conductAppMobilityMeasurement(sys.argv[1], sys.argv[2])
    print("====Application mobility measurement is finished====")
    

