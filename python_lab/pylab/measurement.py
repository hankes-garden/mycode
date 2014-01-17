# -*- coding: utf-8 -*-
'''
Created on 2014年1月16日

@author: jason
'''

from common_function import *
from extract_path import *

import multiprocessing


result_list = []

def log_result(rt):
    for path in rt.values():
        result_list.append(path)
    print("==> "+len(result_list)+" imeis have been processed.")
    
def proc_init():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    nImeiCount = len(lsImeis)
    nPoolSize = min(nImeiCount/IMEI_PER_PROC, MAX_PROC_NUM)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    
    nStartIndex = 0
    while nStartIndex < nImeiCount:
        nEndIndex = min(nStartIndex+IMEI_PER_PROC, nImeiCount)
        pool.apply_async(extractPath, args=(lsImeis[nStartIndex:nEndIndex], strInDir, lsCDRFilePaths, strOutDir), callback = log_result)
        nStartIndex = nEndIndex
    pool.close()
    pool.join()
    
    return result_list
        
def statistic(lsResult):
    text = ""
    for path in lsResult:
        if len(path) != 0:
            info = getPathInfo(path)
            text += info.toString()
            text += "\n"
    return text
        
def pickIMEI(strDistinctedImeisPath):
    '''pick some IMEIs from IMEI list'''
    lsImeis = list()
    with open(strDistinctedImeisPath) as hInFile:
        while(1):
                lsLines = hInFile.readlines(MAX_PROC_MEM)
                if not lsLines:
                    break
                
                for i in xrange(len(lsLines)):
                    if (i%SAMPLING_INTERVAL ==0):
                        strIm = lsLines[i].split(',')[0].strip()
                        if (strIm != "" and strIm.isdigit() ):
                            lsImeis.append(strIm)
    
    return lsImeis
        

        
def conductMeasurement():
    print("begin to pick Imeis...")
    lsImeis = pickIMEI("/mnt/disk7/yanglin/data/distinct_imei.txt")
    print("%d IMEIs need to be processed." % (len(lsImeis)))

    print("begin to extract path for these Imeis...")
    strInDir = "/mnt/disk7/yanglin/data/cdr/"
    lsCDR = [\
            # "new1.dat", \
            # "new2.dat" \
             "export-userservice-2013100307.dat", \
             "export-userservice-2013100308.dat", \
             "export-userservice-2013100309.dat", \
             "export-userservice-2013100310.dat", \
            # "export-userservice-2013100314.dat", \
            # "export-userservice-2013100315.dat", \
            # "export-userservice-2013100316.dat", \
            # "export-userservice-2013100317.dat", \
            # "export-userservice-2013100318.dat", \
            # "export-userservice-2013100319.dat", \
            # "export-userservice-2013100320.dat", \
            ]

    strOutDir = "/mnt/disk7/yanglin/data/out/"
    lsResult = extractPathinParallel(lsImeis, strInDir, lsCDR, strOutDir)

    print("extraction finished, start doing statistics...")
    text = statistic(lsResult)
    if (text != ""):
        strOutFileName = "statistic_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
        with open(strOutDir+strOutFileName, 'w') as hRtFile:
            hRtFile.write(text)
    else:
        print("no result, something must be wrong!")

    print("--measurement done!--")


if __name__ == '__main__':
   conductMeasurement()
