# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
from node import *
from tuple import *
from common_function import *

import multiprocessing


# some global variables
g_max_buffer_size = 0
g_max_buffer_size = 1024*1024*512
result_list = []

def extractPath(strIMEI, lsInFiles, strOutDir):
    '''extract roaming path of given IMEI from CDR'''
    if len(lsInFiles) == 0 :
        raise NameError("Error: empty input file list")
    
    lsPath = list() # the roaming path
    
    for strInFilePath in lsInFiles:
        with open(strInFilePath) as hInFile:
            curNode = CNode("", 0, 0)
            
            while(1):
                lsLines = hInFile.readlines(g_max_buffer_size)
                if not lsLines:
                    break
                
                for line in lsLines:
                    try:
                        if (line.split(',')[4].strip() != strIMEI.strip() ): 
                            continue # not the given user, skip it!
                        
                        # parse line
                        tp = CTuple()
                        tp.parseFromStr(line)
                        
                        if (tp.m_nCellID != curNode.m_nCellID): #enter a new cell
                            newNode = CNode(tp.m_strIMEI, tp.m_nLac, tp.m_nCellID)
                            newNode.m_firstTime = tp.m_firstTime
                            newNode.m_endTime = tp.m_endTime
                            newNode.updateDuration()
                            newNode.m_nRat = tp.m_nRat
                            newNode.m_lsApps.append(tp.m_app)
                            if (curNode.m_nCellID != 0):
                                newNode.m_dMobility_speed = calcMobility(curNode, newNode)
                                
                            lsPath.append(newNode)
                            curNode = newNode
                            
                        else: # still in current cell
                            curNode.m_firstTime = min(curNode.m_firstTime, tp.m_firstTime)
                            curNode.m_endTime = max(curNode.m_firstTime, tp.m_endTime)
                            curNode.updateDuration()
                            
                            index = curNode.findAppIndex(tp.m_app)
                            if (index != -1):  # already exists in the app list
                                curNode.m_lsApps[index].m_nUpPackets += tp.m_app.m_nUpPackets
                                curNode.m_lsApps[index].m_nDownPackets += tp.m_app.m_nDownPackets
                                curNode.m_lsApps[index].m_nUpBytes += tp.m_app.m_nUpBytes
                                curNode.m_lsApps[index].m_dUpSpeed = max(curNode.m_lsApps[index].m_dUpSpeed, tp.m_app.m_dUpSpeed)
                                curNode.m_lsApps[index].m_dDowSpeed = \
                                max(curNode.m_lsApps[index].m_dDownSpeed, tp.m_app.m_dDownSpeed)
                            else: # new app
                                curNode.m_lsApps.append(tp.m_app)
                            
                            lsPath.pop()
                            lsPath.append(curNode)
                        
                    except NameError as err:
                        print(err)

    # Note: all the nodes of given IMEI will first store in MEM and then write to file
#     writePath2File(strIMEI, strOutDir, lsPath)
    strFilePath = serializePath(strIMEI, strOutDir, lsPath)
    return strFilePath


def log_result(rt):
    result_list.append(rt)
    
def proc_init():
    print("Starting proc:", multiprocessing.current_process().name )
    
def fake_extractPath(strIMEI, lsInFiles, strOutDir):
    print("doing " + strIMEI)

def extractPathinParallel(lsImeis, lsCDRFilePaths, strOutDir):
    nPoolSize = min(len(lsImeis), multiprocessing.cpu_count()*2)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    for strImei in lsImeis:
        pool.apply_async(extractPath, args=(strImei, lsCDRFilePaths, strOutDir), callback = log_result)
    pool.close()
    pool.join()
    print(result_list)
    
        
if __name__ == '__main__':
    lsImeis = ["127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["D:\\yanglin\\local\\work\\playground\\t1.csv", \
             "D:\\yanglin\\local\\work\\playground\\t2.csv", \
             "D:\\yanglin\\local\\work\\playground\\t3.csv"]
    strOutDir = "D:\\yanglin\\local\\work\\playground\\"
    extractPathinParallel(lsImeis, lsCDR, strOutDir)

    