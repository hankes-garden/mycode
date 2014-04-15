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
    print("--> %d IMEIs have been found." % (len(g_dcDistinctIMEI)) )

def procInit():
    print("--> Starting proc:" + multiprocessing.current_process().name )

def getDistinctIMEIs(strInCDRDir, strOutPath, lsCDR = None):
    '''
        This function find all distinct IMEIs from CDR data in sequence,
        
        If lsCDR == None, then it will scan all the data under the strInCDRDir

    '''
    # Get CDR list
    lsFiles = lsCDR
    if(lsFiles == None):
        lsFiles = []
        for (dirpath, dirnames, filenames) in os.walk(strInCDRDir):
            for fn in filenames:
                lsFiles.append(dirpath+fn)

#    # create a process pool
#    pool = multiprocessing.Pool(processes=len(lsFiles), initializer=procInit)
#
#    for f in lsFiles:
#        pool.apply_async(getDistinctIMEIs, args=(f,), callback = getIMEICallback)
#
#    pool.close()
#    pool.join()

    # find distinct from files
    for f in lsFiles:
        dc = getDistinctIMEIsFromFile(f)
        g_dcDistinctIMEI.update(dc)
        del dc

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
            lsLines = hInFile.readlines(1024*1024*1024*10)
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
    getDistinctIMEIs("/mnt/disk8/yanglin/data/cdr/", "/mnt/disk8/yanglin/data/out/distinct_imei_full.txt", None)
#    pass
