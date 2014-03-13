# -*- coding: utf-8 -*-
'''
Created on 2014年1月16日

@author: jason
'''

from common_function import *
from extract_path import *
from app_mobility import *

import multiprocessing


g_lsPaths = []

def log_result(rt):
    '''
        merge the paths together
    '''
    for path in rt.values():
        if len(path) != 0 : # drop all the empty paths
            g_lsPaths.append(path)
    print("==> %d users have been processed." % (len(g_lsPaths) ) )
    
def proc_init():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    '''
        start multiple processes to extract path in parallel
    '''
    nImeiCount = len(lsImeis)
    nPoolSize = min(nImeiCount/IMEI_PER_PROC, MAX_PROC_NUM)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    
    nStartIndex = 0
    while nStartIndex < nImeiCount:
        nEndIndex = min(nStartIndex+IMEI_PER_PROC, nImeiCount)
        pool.apply_async(extractPath, args=(dcCellLoc, lsImeis[nStartIndex:nEndIndex], strInDir, lsCDRFilePaths, strOutDir), callback = log_result)
        nStartIndex = nEndIndex
    pool.close()
    pool.join()
    
    return g_lsPaths
        
def statistic(lsResult):
    text = ""
    for path in lsResult:
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
                    if (i%USER_SELECTION_BASE ==0):
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

    # construct cell-location mapping
    print("start building cell-location dict...")
    dcCellLoc = constructCellLocDict(strCellLocRefPath)
    print("cell-location dict is finished, #cell-location=%d" % (len(dcCellLoc)))

    # extract roaming path in parallel
    print("start path extraction...")
    lsPaths = extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDR, strOutDir)
    print("path extraction is finished")
    
    # serialize roaming path
    # TODO: change the file name
    print("start serialization of path...")
    strPathListName = "serPath_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
    serialize2File(strPathListName, strOutDir, lsPaths)
    print("serialization of path is finished.")
    
    # path statistics
    print("Start path statistics...")
    strStatisticName = "statistic_%d_%s_%s.txt" % (len(lsImeis), lsCDR[0].split('.')[0], lsCDR[-1].split('.')[0])
    text = statistic(lsPaths)
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
     
#     # setup for mh1
#     strImeisPath = "/mnt/disk12/yanglin/data/distinct_imei.txt"
#     strCellLocRefPath = "/mnt/disk12/yanglin/data/dict.csv"
#     strInDir = "/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/"
#     lsCDR = [\
#             "export-userservice-2013100318.dat", \
#             "export-userservice-2013100319.dat", \
#             "export-userservice-2013100320.dat", \
#             "export-userservice-2013100321.dat" \
#             ]
#     strOutDir = "/mnt/disk12/yanglin/data/out/"
    
    # setup for mh2/mh5
    strImeisPath = "/mnt/disk7/yanglin/data/distinct_imei.txt"
    strCellLocRefPath = "/mnt/disk7/yanglin/data/dict.csv"
    strInDir = "/mnt/disk7/yanglin/data/cdr/"
    lsCDR = [\
            "export-userservice-2013100312.dat", \
            "export-userservice-2013100313.dat", \
            "export-userservice-2013100314.dat", \
            "export-userservice-2013100315.dat" \
            ]
    strOutDir = "/mnt/disk7/yanglin/data/out/"

    conductMeasurement(strCellLocRefPath, strImeisPath, strInDir, lsCDR, strOutDir)
