# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from node import *
from pathinfo import *
from my_error import MyError

import time
import cPickle
import gc

import os

MAX_IO_BUF_SIZE = 0
MAX_IO_BUF_SIZE = 1024*1024*1024*1

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

def calculateMobilitySpeed(node1, node2):
    '''
        Calculate moving speed
        Unit: m/s
    '''
    if(node1.m_dLat == 0.0 or node1.m_dLong == 0.0 or node2.m_dLat == 0.0 or node2.m_dLong == 0.0 ):
        return 0
    
    nDistance = calculateDistance(node1.m_dLat, node1.m_dLong, node2.m_dLat, node2.m_dLong)
    dDuration = node1.m_dDuration + node2.m_dDuration
    dSpeed = 2.0*nDistance//dDuration
    if dSpeed < 0:
        raise MyError("invalid speed,duration=%.2f, distance=%d, n1.start=%s, n2.end=%s" % \
                            (dDuration, nDistance, get_time_str(node1.m_firstTime), get_time_str(node2.m_endTime) ) )
    return dSpeed
    


def getPathInfo(path):
    '''compute statistic for each roaming path'''
    info = CPathInfo()
    info.m_nPathLen = len(path.m_lsNodes)
    info.m_strIMEI = path.m_strIMEI
    for x in path.m_lsNodes:
        info.m_dMobility += x.m_dSpeed
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
    
    if (len(path.m_lsNodes) != 0):
        info.m_dAvgUpSpeed = info.m_dAvgUpSpeed / len(path.m_lsNodes)
        info.m_dAvgDownSpeed = info.m_dAvgDownSpeed / len(path.m_lsNodes)
        info.m_dMobility = info.m_dMobility / len(path.m_lsNodes) # overall mobility = average of mobility of each node
        
    return info

  
def write2File(strContent, strOutFilePath):
    if len(strOutFilePath) != 0:
        with open(strOutFilePath, 'w') as hOutFile:
            hOutFile.write(strContent)
    else:
        raise MyError("Error: invalid output file path")
    

def serialize2File(strOutFilePath, obj):
    if len(obj) != 0:
        with open(strOutFilePath, 'w') as hOutFile:
            cPickle.dump(obj, hOutFile, protocol=-1)
    else:
        print("Nothing to serialize!")
   

def deserializeFromFile(strFilePath):
    obj = 0
    with open(strFilePath) as hFile:
        obj = cPickle.load(hFile)
    return obj

def findOutliers(lsPaths, nCriterion):
    for path in lsPaths:
        if len(path.m_lsNodes) >= nCriterion:
            print("Abnormal user: imei=%s, #path=%d" % (path.m_strIMEI, len(path.m_lsNodes) ) )
            
def traceUser(lsPaths, strImei):
    print("--Trace user:%s start--" % strImei)
    for path in lsPaths:
        if path.m_strIMEI == strImei:
            for node in path.m_lsNodes:
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
        format: nlac-cid, lat, long
    '''
    dcCellLoc = {}
    with open(strLocationDictPath) as hLocDict:
        hLocDict.readline() # skip head
        for line in hLocDict:
            items = line.split(',')
            key = items[0]
            if(key!=""):
                value = (0., 0.)
                try:
                    if (items[1]!="" and items[2]!=""):
                        value = (float(items[1]), float(items[2]) )
                except IndexError:
                    print "Line:" + line
                    raise
                dcCellLoc[key] = value

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
    arc = math.acos( 1.0 if cos>1.0 else cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6373 * 1000 # get distance in meters

import pandas as pd
def getServiceDict(strServiceDictPath):
    dfService = pd.read_csv(strServiceDictPath, index_col='ServiceType')
    return dfService

def outputLocalAppLocation(dcLocalApp, strOutPath):
    with open(strOutPath, 'w') as hOutFile:
        hOutFile.write("serviceType, lac-cid, lat, long, attributes\n")
        for nServiceType in dcLocalApp.keys():
            lsTopCells = dcLocalApp.get(nServiceType)
            for tp in lsTopCells:
                strLine = "%d, %s,%.6f,%.6f, %d\n" % (nServiceType, tp[0], tp[1][0], tp[1][1], tp[2])
                hOutFile.write(strLine)
            
def ensurePathExist(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
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

def calculateRog(path):
    '''
        rog = sqrt(1/n*sum(power(dis(mass, node), 2) ) )
    '''
    dRog = 0.0
    if(len(path.m_lsNodes) != 0):
        dMassLat = 0.0
        dMassLong = 0.0
        nKnownNodeNum = 0
        
        for node in path.m_lsNodes:
            if (node.m_dLat != 0.0 and node.m_dLong != 0.0):
                nKnownNodeNum += 1
                dMassLat += node.m_dLat
                dMassLong += node.m_dLong
                
        if (nKnownNodeNum > 0 ):
            dMassLat = dMassLat / nKnownNodeNum
            dMassLong = dMassLong / nKnownNodeNum
            
            dVariance = 0.0
            for node in path.m_lsNodes:
                if (node.m_dLat != 0.0 and node.m_dLong != 0.0):
                    dDis = calculateDistance(node.m_dLat, node.m_dLong, dMassLat, dMassLong)
                    dVariance += math.pow(dDis, 2)
            dRog = math.sqrt(dVariance/nKnownNodeNum)

        
    return dRog


def updateDictBySum(dc, key, newValue):
    if key in dc:
        dc[key] += newValue
    else:
        dc[key] = newValue
        
def updateDictBySumOnAttribute(dcApps, lsApps, strAttributeName):
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

if __name__ == '__main__':
    print("this is common function")
#      dc = constructCellLocDict("d:\\playground\\dict.csv")
#      try:
#          maxPair = (("dd",(0,0)), ("ee", (0,0)))
#          dMaxDistance = 0.0
#          for i in dc.items():
#              for j in dc.items():
#                  if i[0] != j[0]:
#                      dis = calculateDistance(i[1][0], i[1][1], j[1][0], j[1][1])
#                      if (dis > dMaxDistance):
#                          dMaxDistance = dis
#                          maxPair = (i,j)
#                      
#                      print("max=%.2f, from (%.6f, %.6f) to (%.6f, %.6f)" % \
#                            (dMaxDistance/1000, maxPair[0][1][0], maxPair[0][1][1],\
#                             maxPair[1][1][0],maxPair[1][1][1]\
#                                                         ) )
#      
#      except ValueError:
#          pass
#                     
  
