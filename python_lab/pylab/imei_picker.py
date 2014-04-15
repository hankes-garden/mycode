# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 22:11:00 2014

@author: jason
"""
from common_function import *

import pandas as pd
import os
import multiprocessing

g_dcDistinctIMEI = {}

def getIMEICallback(ret):
    g_dcDistinctIMEI.update(ret)
    del ret
    print("--> %d IMEIs have been found." % (len(g_dcDistinctIMEI)) )

def getIMEIInit():
    print("--> Starting proc:" + multiprocessing.current_process().name )

def getDistinctIMEIs(strInCDRDir, strOutPath, lsCDR = None):
    '''
        This function find all distinct IMEIs from CDR data in sequence,
        
        If lsCDR == None, then it will scan all the data under the strInCDRDir

    '''
    # Get CDR list
    lsCDR = lsCDR
    if(lsCDR == None):
        lsCDR = []
        for (dirpath, dirnames, filenames) in os.walk(strInCDRDir):
            for fn in filenames:
                lsCDR.append(dirpath+fn)

    # create a process pool
    pool = multiprocessing.Pool(processes=5, initializer=getIMEIInit)

    for f in lsCDR:
        pool.apply_async(getDistinctIMEIsFromFile, args=(f,), callback = getIMEICallback)

    pool.close()
    pool.join()

#    # find distinct from files
#    for f in lsCDR:
#        dc = getDistinctIMEIsFromFile(f)
#        g_dcDistinctIMEI.update(dc)
#        del dc

    #write to file
    del g_dcDistinctIMEI['']
    with open(strOutPath, 'w') as hOutFile:
        for imei in g_dcDistinctIMEI.keys():
            if (pd.isnull(imei) or imei==''):
                continue
            hOutFile.write("%s\n" % imei.strip())


    return g_dcDistinctIMEI

def getDistinctIMEIsFromFile(strCDR):
    print("--> Scanning file: %s" % strCDR)
    
    dc = {}
    with open(strCDR) as hInFile:
        hInFile.readline() # skip head
        while(1):
            print("--> reading...")
            lsLines = hInFile.readlines(1024*1024*1024*5)
            if not lsLines: # break if there is no more lines
                break
            
            print("--> sampling...")
            for line in lsLines:
                lsItems = line.split(",")
                if(len(lsItems) != 31):
                    continue
                dc[lsItems[4]] = 0
                
            del lsLines
    return dc

if __name__ == '__main__':
    getDistinctIMEIs("/mnt/disk3/yanglin/data/cdr/", "/mnt/disk3/yanglin/data/out/distinct_imei_full.txt", None)
#    pass
