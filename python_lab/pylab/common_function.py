# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from node import *
from pathinfo import *

import time
import cPickle

MAX_IO_BUF_SIZE = 0
MAX_IO_BUF_SIZE = 1024*1024*1024*1

USER_SELECTION_BASE = 100 # there are about 7 million users, #selectedUser=7million\base
MAX_PROC_NUM = 15
IMEI_PER_PROC = 300 # how many Imeis should be processed in each process

def exeTime(func):
    '''
    NOTE: Decorator will raise pickleError in MultiProcess!!
    '''
    def newFunc(*args, **args2):
        t0 = time.time()
        print "%s: func_%s starts" % (time.strftime("%X", time.localtime()), func.__name__)
        back = func(*args, **args2)
        print "%s: func_%s ends" % (time.strftime("%X", time.localtime()), func.__name__)
        print ">>func_%s takes %.3f seconds" % (func.__name__, time.time() - t0)
        return back
    return newFunc

def format_result(s, up_bytes, app, port):
    '''format my output'''
    x = time.localtime(s)
    text = '%s,%s,%s,%s\n' % (time.strftime('%Y%m%d %H:%M:%S', x), up_bytes, app, port)
    return text

def reformat_time_string(str_time):
    '''reformat the time string in the CDR and return a integer in UTC'''
    str_tmp = str_time.split('.')[0] # delete numbers after decimal
    str_time = str_tmp[0:10] + " " + str_tmp[10:18]
    t = time.strptime(str_time,'%Y-%m-%d %H:%M:%S')
    return t

def get_time_str(tm):
    return time.strftime('%Y%m%d %H:%M:%S', tm)

def calcMobility(node1, node2):
    '''
        Calculate moving speed
        
    '''
    # TODO: define the mobility btw nodes
    if(node1.m_dLat == 0.0 or node2.m_dLat == 0.0):
        return 0
    nDistance = calculateDistance(node1.m_dLat, node1.m_dLong, node2.m_dLat, node2.m_dLong)
    dDuration = time.mktime(node2.m_endTime) - time.mktime(node1.m_firstTime)
    dMob = 2*nDistance / dDuration
    
    return dMob
    


def getPathInfo(lsPath):
    '''compute statistic for each roaming path'''
    info = CPathInfo()
    info.m_nPathLen = len(lsPath)
    info.m_strIMEI = lsPath[0].m_strIMEI
    for x in lsPath:
        info.m_dMobility += x.m_dMobility_speed
        for y in x.m_lsApps:
            # uplink
            info.m_nUpBytes += y.m_nUpBytes
            info.m_nUpPackets += y.m_nUpPackets
            info.m_dAvgUpSpeed += y.m_dUpSpeed
            if info.m_dMaxUpSpeed < y.m_dUpSpeed:
                info.m_dMaxUpSpeed = y.m_dUpSpeed
            if info.m_dMinUpSpeed > y.m_dUpSpeed:
                info.m_dMinUpSpeed = y.m_dUpSpeed
            
            # downlink
            info.m_nDownBytes += y.m_nDownBytes
            info.m_nDownPackets += y.m_nDownPackets
            info.m_dAvgDownSpeed += y.m_dDownSpeed
            if info.m_dMaxDownSpeed < y.m_dDownSpeed:
                info.m_dMaxDownSpeed = y.m_dDownSpeed
            if info.m_dMinDownSpeed > y.m_dDownSpeed:
                info.m_dMinDownSpeed = y.m_dDownSpeed
    
    if (len(lsPath) != 0):
        info.m_dAvgUpSpeed = info.m_dAvgUpSpeed / len(lsPath)
        info.m_dAvgDownSpeed = info.m_dAvgDownSpeed / len(lsPath)
        info.m_dMobility = info.m_dMobility / len(lsPath) # overall mobility = average of mobility of each node
        
    return info

def writePath2File(strIMEI, strOutDir, lsPath):
    if len(lsPath) != 0:
        text = ""
        for x in lsPath:
            text += x.toString()
            text += "\n"
         
        # get path info
        info = getPathInfo(lsPath)
        text += info.toString()
        strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(lsPath), strIMEI)
        with open(strOutFilePath, 'w') as hOutFile:
            hOutFile.write(text)
    else:
        raise StandardError("Error: Empty roaming path")
    
def write2File(strContent, strOutFilePath):
    if len(strOutFilePath) != 0:
        with open(strOutFilePath, 'w') as hOutFile:
            hOutFile.write(strContent)
    else:
        raise StandardError("Error: invalid output file path")
    

def serialize2File(strFileName, strOutDir, obj):
    if len(obj) != 0:
        strOutFilePath = "%s%s" % (strOutDir, strFileName)
        with open(strOutFilePath, 'w') as hOutFile:
            cPickle.dump(obj, hOutFile, protocol=0)
        return strOutFilePath
    else:
        print("Nothing to serialize!")
   

def deserializeFromFile(strFilePath):
    obj = 0
    with open(strFilePath) as hFile:
        obj = cPickle.load(hFile)
    return obj

def findOutliers(lsPaths, nCriterion):
    for path in lsPaths:
        if len(path) >= nCriterion:
            print("Abnormal user: imei=%s, #path=%d" % (path[0].m_strIMEI, len(path) ) )
            
def traceUser(lsPaths, strImei):
    print("--Trace user:%s start--" % strImei)
    for path in lsPaths:
        if path[0].m_strIMEI == strImei:
            for node in path:
                nUpBytes = 0
                nDownBytes = 0
                strApp = ""
                for app in node.m_lsApps:
                    nUpBytes += app.m_nUpBytes
                    nDownBytes += app.m_nDownBytes
                print("node: lac=%d, cellID=%d, duration=%.2f, upBytes=%d, downBytes=%d, %s, %s" % \
                      (node.m_nLac, node.m_nCellID, node.m_dDuration,\
                       nUpBytes, nDownBytes,\
                       get_time_str(node.m_firstTime), get_time_str(node.m_endTime)))
                
    print("--Trace user end--")
    
    
def constructCellLocDict(strLocationDictPath):
    ''''
        construction a dictionary for cell-location mapping
    '''
    dcCellLoc = {}
    with open(strLocationDictPath) as hLocDict:
        while(1):
            hLocDict.readline() # skip head
            lsLines = hLocDict.readlines(MAX_IO_BUF_SIZE)
            if not lsLines:
                break
            try:
                for line in lsLines:
                    items = line.split(',')
                    key = items[2]
                    value = (float(items[3]), float(items[4]) )
                    dcCellLoc[key] = value
            except ValueError:
                pass
    return dcCellLoc


import math
def calculateDistance(lat1, long1, lat2, long2):

    if (lat1==lat2 and long1==long2):
        return 0
    
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6373 * 1000 # get distance in meters
            
            
            
                
if __name__ == '__main__':
    dc = constructCellLocDict("d:\\playground\\dict.csv")
    
    try:
        maxPair = (("dd",(0,0)), ("ee", (0,0)))
        dMaxDistance = 0.0
        for i in dc.items():
            for j in dc.items():
                if i[0] != j[0]:
                    dis = calculateDistance(i[1][0], i[1][1], j[1][0], j[1][1])
                    if (dis > dMaxDistance):
                        dMaxDistance = dis
                        maxPair = (i,j)
                    
                    print("max=%.2f, from (%.6f, %.6f) to (%.6f, %.6f)" % \
                          (dMaxDistance/1000, maxPair[0][1][0], maxPair[0][1][1],\
                           maxPair[1][1][0],maxPair[1][1][1]\
                                                       ) )
    
    except ValueError:
        pass
                    
  
    