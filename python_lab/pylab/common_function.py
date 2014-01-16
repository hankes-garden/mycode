# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from node import *
from pathinfo import *

import time
import cPickle

def exeTime(func):
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
    '''calculate moving speed'''
    return 1.0


def getPathInfo(lsPath):
    '''compute statistic for each roaming path'''
    mb = CPathInfo()
    mb.m_nPathLen = len(lsPath)
    mb.m_strIMEI = lsPath[0].m_strIMEI
    for x in lsPath:
        mb.m_dMobility += x.m_dMobility_speed
        for y in x.m_lsApps:
            # uplink
            mb.m_nUpBytes += y.m_nUpBytes
            mb.m_nUpPackets += y.m_nUpPackets
            if mb.m_dMaxUpSpeed < y.m_dUpSpeed:
                mb.m_dMaxUpSpeed = y.m_dUpSpeed
            if mb.m_dMinUpSpeed > y.m_dUpSpeed:
                mb.m_dMinUpSpeed = y.m_dUpSpeed
            
            #downlink
            mb.m_nDownBytes += y.m_nDownBytes
            mb.m_nDownPackets += y.m_nDownPackets
            if mb.m_dMaxDownSpeed < y.m_dDownSpeed:
                mb.m_dMaxDownSpeed = y.m_dDownSpeed
            if mb.m_dMinDownSpeed > y.m_dDownSpeed:
                mb.m_dMinDownSpeed = y.m_dDownSpeed
    
    mb.m_dMobility = mb.m_dMobility / len(lsPath) # overall mobility = average of mobility of each node
    
    return mb

def writePath2File(strIMEI, strOutDir, lsPath):
    if len(lsPath) != 0:
        text = ""
        for x in lsPath:
            text += x.toString()
            text += "\n"
         
        # get path info
        info = common_function.getPathInfo(lsPath)
        text += info.toString()
        strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(lsPath), strIMEI)
        with open(strOutFilePath, 'w') as hOutFile:
            hOutFile.write(text)
    else:
        raise NameError("Error: Empty roaming path")
    

def serializePath(strIMEI, strOutDir, lsPath):
    if len(lsPath) != 0:
        strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(lsPath), strIMEI)
        with open(strOutFilePath, 'w') as hOutFile:
            cPickle.dump(lsPath, hOutFile, protocol=0)
        return strOutFilePath
    else:
        raise NameError("Error: Empty roaming path")
   

def deserializePath(strFilePath):
    lsPath = 0
    with open(strFilePath) as hFile:
        lsPath = cPickle.load(hFile)
    return lsPath
    
if __name__ == '__main__':
    print('This is a common module which includes many useful functions')
    