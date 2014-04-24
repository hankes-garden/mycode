# -*- coding: utf-8 -*-
'''
Created on 2014年1月16日

@author: jason

This module will extract user's roaming path from raw CDR data in parallel,
and serialize result dict to disk.
'''

from common_function import *
from extract_path import *
from app_mobility import *


import multiprocessing
import math
import os


g_nUser2Process = 0             # Total User to be processed
g_nMaxProcessNum = 20           # number of processes running in parallel
g_nUserPerProcess = 100         # how many Imeis should be processed in each process
g_nUser2Simple = 0              # How to select user?
g_nStartIndex = 0               # the start index of distinct_user_dict
g_nEndIndex = 0                 # the end index of distinct_user_dict
g_nSerializationID = 0          # the id of current serialization
g_strSerPathPrefix = ''         # the prefix of output path
g_nUserProcessed = 0            # number of processed users


def extractPathCallback(rt):
    '''
        serialize path to file
    '''
    global g_nUserProcessed
    g_nUserProcessed += len(rt)
    
    # serialize dcPaths
    global g_strSerPathPrefix
    if ('' == g_strSerPathPrefix):
        print("--> WTF!!!!! the path is empty~")
        g_strSerPathPrefix = "/mnt/disk2/yanglin/data/out/ser_path/path"
        ensurePathExist(g_strSerPathPrefix)
        
    strOutPath = "%s_%d.txt" % (g_strSerPathPrefix, g_nSerializationID)
    serialize2File(strOutPath, rt)
    g_nSerializationID += 1
    
    print("==> Progress of path extraction: %d of %d" % (g_nUserProcessed, g_nUser2Process) )
    
    del rt

    
def extractPathInit():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    '''
        start multiple processes to extract path in parallel
    '''
    global g_nUser2Process
    nStartIndex = g_nStartIndex
    nImeiEnd = min(len(lsImeis), g_nEndIndex)
    g_nUser2Process = nImeiEnd - nStartIndex
    print("IMEI index:%d ~ %d, #user_to_process = %d" % (nStartIndex, nImeiEnd, g_nUser2Process) )

    nPoolSize = int(min(math.ceil(float(nImeiEnd-nStartIndex)/g_nUserPerProcess), g_nMaxProcessNum))
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=extractPathInit)
    while nStartIndex < nImeiEnd:
        nEndIndex = min(nStartIndex+g_nUserPerProcess, nImeiEnd)
        pool.apply_async(extractPath, args=(dcCellLoc, lsImeis[nStartIndex:nEndIndex], strInDir, lsCDRFilePaths, strOutDir), callback = extractPathCallback)
        nStartIndex = nEndIndex
    pool.close()
    pool.join()
    
def statistic(dcResult):
    text = ""
    for path in dcResult.values():
        if len(path) != 0:
            info = getPathInfo(path)
            text += info.toString()
            text += "\n"
    return text
        
def pickIMEI(strDistinctedImeisPath, bAll = True):
    '''
        pick some IMEIs from IMEI list randomly
        if bAll == True, then pick all IMEIs
    '''
    lsImeis = []
    nBase = 1 if (bAll == True) else int(7000000/g_nUser2Simple)
    with open(strDistinctedImeisPath) as hInFile:
        i = 0
        for line in hInFile:
            if (i%nBase ==0):
                strIm = line.split(',')[0].strip()
                if (strIm != "" and strIm.isdigit() ):
                    lsImeis.append(strIm)
            i += 1
    return lsImeis
        

        
def extract(strCellLocDictPath, strDistinctImeiPath, strInDir, lsCDR, strOutDir, bAll):
    '''
        The main function to conduct all the path extraction, including:
        1. select users
        2. prepare the cell-location mapping
        3. extract path in parallel
        4. serialize path to disk
        5. conduct statistic or sub-domain measurement
    '''
    print("====Begin Path Extraction====")
    print(" cell_loc_dict: %s\n distinct_imei: %s\n input_path: %s\n output_path:%s\n max_proc: %d\n #user_per_proc: %s\n bAll: %s\n" % \
          (strCellLocDictPath, strDistinctImeiPath, strInDir, strOutDir, \
           g_nMaxProcessNum, g_nUserPerProcess,
           "True" if bAll else "False") )
    
    # pick users
    print("start user sampling...")
    lsImeis = pickIMEI(strDistinctImeiPath, bAll)
    print("user sampling is finished, %d IMEIs need to be processed." % (len(lsImeis)))

    # construct cell-location mapping
    print("start building cell-location dict...")
    dcCellLoc = constructCellLocDict(strCellLocDictPath)
    print("cell-location dict is finished, #cell-location=%d" % (len(dcCellLoc)))

    # extract roaming path in parallel
    global g_strSerPathPrefix
    g_strSerPathPrefix = "%sser_path/path_%d_%s_%s" % \
    (strOutDir, len(lsImeis), lsCDR[0].split('.')[0].split('-')[2], lsCDR[-1].split('.')[0].split('-')[2])
    ensurePathExist(g_strSerPathPrefix)

    print("start path extraction...")
    extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDR, strOutDir)
    print("path extraction is finished")
    
#     # serialize roaming path
#     print("start serialization of path...")
#     strPathListName = "serPath_%d_%s_%s" % \
#     (len(lsImeis), lsCDR[0].split('.')[0].split('-')[2], lsCDR[-1].split('.')[0].split('-')[2])
#     serialize2File(strPathListName, strOutDir, dcPaths)
#     print("serialization of path is finished.")
    
    print("====Path Extraction is finished====")


if __name__ == '__main__':
    # running config
    # sys.argv[1] - #user to sample, -1 means all users
    # sys.argv[2] - Max number of sub-process, 10 would be better
    # sys.argv[3] - #user to process in each process, 100,000 would be better
    # sys.argv[4] - working dir
    # sys.argv[5] - start index of distinct_user_dict
    # sys.argv[6] - end index of distinct_user_dict
    if(len(sys.argv) != 7):
        raise MyError("Usage: python path_extractor.py #user2simple, max_proc_number=10, #user_per_proc=100000, working_dir=/mnt/disk7/yanglin/, startIndex, endIndex")
    
    g_nUser2Simple = int(sys.argv[1])
    bAll = True if (g_nUser2Simple == -1) else False
    g_nMaxProcessNum = int(sys.argv[2])
    g_nUserPerProcess = int(sys.argv[3])
    strWorkingDir = sys.argv[4] if sys.argv[4].endswith("/") else sys.argv[4]+"/"
    g_nStartIndex = int(sys.argv[5])
    g_nEndIndex = int(sys.argv[6])
   
    # data setup
    strImeisPath = strWorkingDir + "data/distinct_imei_full.txt"
    strCellLocPath = strWorkingDir + "data/cell_loc_filled.txt"
    strInDir = strWorkingDir + "data/cdr/"
    lsCDR = []
    for (dirpath, dirnames, filenames) in os.walk(strInDir):
        for fn in filenames:
            lsCDR.append(dirpath+fn)
            
    strOutDir = strWorkingDir + "data/out/"
    ensurePathExist(strOutDir)
    extract(strCellLocPath, strImeisPath, strInDir, lsCDR, strOutDir, bAll)
