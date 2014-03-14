# -*- coding: utf-8 -*-
'''
Created on 2014年1月16日

@author: jason
'''

from common_function import *
from extract_path import *
from app_mobility import *


import multiprocessing
import math


g_dcPaths = {}              # extracted paths
g_nUser2Process = 0         # Total User to be processed
g_nUserSelectionBase = 1    # User selection Freq
g_nMaxProcessNum = 20       # number of processes running in parallel
g_nUserPerProcess = 100     # how many Imeis should be processed in each process

def log_result(rt):
    '''
        merge the paths together
    '''
    g_dcPaths.update(rt)
    print("==> path extraction progress: %.2f" % (len(g_dcPaths)/g_nUser2Process ) )
    
def proc_init():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    '''
        start multiple processes to extract path in parallel
    '''
    nImeiCount = len(lsImeis)
    nPoolSize = min(nImeiCount/g_nUserPerProcess, g_nMaxProcessNum)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    
    nStartIndex = 0
    while nStartIndex < nImeiCount:
        nEndIndex = min(nStartIndex+g_nUserPerProcess, nImeiCount)
        pool.apply_async(extractPath, args=(dcCellLoc, lsImeis[nStartIndex:nEndIndex], strInDir, lsCDRFilePaths, strOutDir), callback = log_result)
        nStartIndex = nEndIndex
    pool.close()
    pool.join()
    
    return g_dcPaths
        
def statistic(dcResult):
    text = ""
    for path in dcResult.values():
        if len(path) != 0:
            info = getPathInfo(path)
            text += info.toString()
            text += "\n"
    return text
        
def pickIMEI(strDistinctedImeisPath):
    '''
        pick some IMEIs from IMEI list randomly
    '''
    lsImeis = list()
    with open(strDistinctedImeisPath) as hInFile:
        while(1):
                lsLines = hInFile.readlines(MAX_IO_BUF_SIZE)
                if not lsLines:
                    break
                
                for i in xrange(len(lsLines)):
                    if (i%g_nUserSelectionBase ==0):
                        strIm = lsLines[i].split(',')[0].strip()
                        if (strIm != "" and strIm.isdigit() ):
                            lsImeis.append(strIm)
    
    return lsImeis
        

        
def conductMeasurement(strCellLocRefPath, strImeiPath, strInDir, lsCDR, strOutDir):
    '''
        the main function to conduct all the measurement
    '''
    
    print("--Start Measurement...--")
    
    # pick users
    print("start user selection...")
    lsImeis = pickIMEI(strImeiPath)
    print("user selection is finished, %d IMEIs need to be processed." % (len(lsImeis)))
    g_nUser2Process = len(lsImeis)

    # construct cell-location mapping
    print("start building cell-location dict...")
    dcCellLoc = constructCellLocDict(strCellLocRefPath)
    print("cell-location dict is finished, #cell-location=%d" % (len(dcCellLoc)))

    # extract roaming path in parallel
    print("start path extraction...")
    dcPaths = extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDR, strOutDir)
    print("path extraction is finished")
    
    # serialize roaming path
    # TODO: change the file name
    print("start serialization of path...")
    strPathListName = "serPath_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
    serialize2File(strPathListName, strOutDir, dcPaths)
    print("serialization of path is finished.")
    
    # path statistics
    print("Start path statistics...")
    strStatisticName = "statistic_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
    text = statistic(dcPaths)
    if (text != ""):
        with open(strOutDir+strStatisticName, 'w') as hRtFile:
            hRtFile.write(text)
    else:
        raise StandardError("empty statistic.")
    print("Path statistics is finished.")
        
    # application mobility measurement
    print("Start application mobility measurement...")
    strAppMobilityName = "appmob_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
    conductAppMobilityMeasurement(strOutDir+strPathListName, strOutDir+strAppMobilityName)
    print("Application mobility measurement is finished")

    print("--All measurements are finished--")


if __name__ == '__main__':
    # running config
    g_nUser2Process = int(sys.argv[1])
    if(g_nUser2Process > TOTAL_USER_NUMBER or g_nUser2Process == 0):
        raise StandardError("Error: trying to extrac %d user from all 7,000,000 users" % (g_nUser2Process) )
    g_nUserSelectionBase = math.ceil(float(TOTAL_USER_NUMBER)/float(g_nUser2Process))
    
    g_nMaxProcessNum = int(sys.argv[2])
    g_nUserPerProcess = int(sys.argv[3])
   
    # data setup
    strImeisPath = "/mnt/disk8/yanglin/data/distinct_imei.txt"
    strCellLocRefPath = "/mnt/disk8/yanglin/data/dict.csv"
    strInDir = "/mnt/disk8/yanglin/data/cdr/"
    lsCDR = [\
            "export-userservice-2013090922.dat", \
#             "export-userservice-2013090919.dat", \
#             "export-userservice-2013090920.dat", \
#             "export-userservice-2013090921.dat" \
            ]
    strOutDir = "/mnt/disk8/yanglin/data/out/"

    conductMeasurement(strCellLocRefPath, strImeisPath, strInDir, lsCDR, strOutDir)
