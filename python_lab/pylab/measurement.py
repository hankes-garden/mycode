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
    if (len(rt) != 0):
        result_list.append(rt)
    
def proc_init():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    nPoolSize = min(len(lsImeis), 10)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    for strImei in lsImeis:
        pool.apply_async(extractPath, args=(strImei, strInDir, lsCDRFilePaths, strOutDir), callback = log_result)
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
    lsImeis = pickIMEI("/mnt/disk12/yanglin/workspace/distinct_imei.txt")
    print("picked %d IMEIs to extrac." % (len(lsImeis)))

    print("begin to extract path for these Imeis...")
    strInDir = "/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/"
    lsCDR = [\
            # "new1.dat", \
             "export-userservice-2013100308.dat", \
             "export-userservice-2013100309.dat" \
            # "export-userservice-2013100312.dat", \
            # "export-userservice-2013100313.dat", \
            # "export-userservice-2013100314.dat", \
            # "export-userservice-2013100315.dat", \
            # "export-userservice-2013100316.dat", \
            # "export-userservice-2013100317.dat", \
            # "export-userservice-2013100318.dat", \
            # "export-userservice-2013100319.dat", \
            # "export-userservice-2013100320.dat" \
            ]

    strOutDir = "/mnt/disk12/yanglin/workspace/paths/"
    lsResult = extractPathinParallel(lsImeis, strInDir, lsCDR, strOutDir)

    print("extraction finished, start doing statistics...")
    text = statistic(lsResult)
    if (text != ""):
        with open(strOutDir+"result.txt", 'w') as hRtFile:
            hRtFile.write(text)
    else:
        print("no result, something must be wrong!")

    print("--measurement done!--")


if __name__ == '__main__':
   conductMeasurement()
