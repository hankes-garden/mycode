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
    '''calculate moving speed'''
    return 0


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
    
if __name__ == '__main__':
    print('This is a common module which includes many useful functions')
    