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


g_dcPaths = {}              # global extracted paths
g_nUser2Process = 0         # Total User to be processed
g_nUserSelectionBase = 1    # User selection Freq
g_nMaxProcessNum = 20       # number of processes running in parallel
g_nUserPerProcess = 100     # how many Imeis should be processed in each process

def extractPathCallback(rt):
    '''
        merge the paths together
    '''
    global g_nUserPerProcess
    
    g_dcPaths.update(rt)
    print("==> Progress of path extraction: %.2f" % ( float(len(g_dcPaths))/g_nUser2Process*100.0 ) + "%")
    
def proc_init():
    print("Starting proc:" + multiprocessing.current_process().name )
    
def extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDRFilePaths, strOutDir):
    '''
        start multiple processes to extract path in parallel
    '''
    nImeiCount = len(lsImeis)
    nPoolSize = int(min(math.ceil(float(nImeiCount)/g_nUserPerProcess), g_nMaxProcessNum))
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    
    nStartIndex = 0
    while nStartIndex < nImeiCount:
        nEndIndex = min(nStartIndex+g_nUserPerProcess, nImeiCount)
        pool.apply_async(extractPath, args=(dcCellLoc, lsImeis[nStartIndex:nEndIndex], strInDir, lsCDRFilePaths, strOutDir), callback = extractPathCallback)
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
        

        
def conductMeasurement(strCellLocPath, strImeiPath, strInDir, lsCDR, strOutDir):
    '''
        The main function to conduct all the measurement, including:
        1. select users
        2. prepare the cell-location mapping
        3. extract path in parallel
        4. serialize path to disk
        5. conduct statistic or sub-domain measurement
    '''
    global g_nUser2Process

    print("--Measurement configuration--")
    print(" cell_Loc_path: %s\n IMEI_path: %s\n input_path: %s\n output_path:%s\n #user:%s\n max_proc: %d\n #user_per_proc: %s\n" % \
          (strCellLocPath, strImeiPath, strInDir, strOutDir, \
           g_nUser2Process, g_nMaxProcessNum, g_nUserPerProcess) )
    
    print("--Start Measurement...--")
    # pick users
    print("start user selection...")
    lsImeis = pickIMEI(strImeiPath)
    print("user selection is finished, %d IMEIs need to be processed." % (len(lsImeis)))
    g_nUser2Process = len(lsImeis)

    # construct cell-location mapping
    print("start building cell-location dict...")
    dcCellLoc = constructCellLocDict(strCellLocPath)
    print("cell-location dict is finished, #cell-location=%d" % (len(dcCellLoc)))

    # extract roaming path in parallel
    print("start path extraction...")
    dcPaths = extractPathinParallel(dcCellLoc, lsImeis, strInDir, lsCDR, strOutDir)
    print("path extraction is finished")
    
    # serialize roaming path
    print("start serialization of path...")
    strPathListName = "serPath_%d_%s_%s.txt" % \
    (len(lsImeis), lsCDR[0].split('.')[0].split('-')[2], lsCDR[-1].split('.')[0].split('-')[2])
    serialize2File(strPathListName, strOutDir, dcPaths)
    print("serialization of path is finished.")
    
    # application mobility measurement
    print("Start application mobility measurement...")
    strAppMobilityName = "appmob_%d_%s_%s" % \
    (len(lsImeis), lsCDR[0].split('.')[0].split('-')[2], lsCDR[-1].split('.')[0].split('-')[2])
    conductAppMobilityMeasurement(strOutDir+strPathListName, strOutDir+strAppMobilityName, dcPaths)
    print("Application mobility measurement is finished")

    print("--All measurements are finished--")


if __name__ == '__main__':
    # running config
    # sys.argv[1] - #user to process
    # sys.argv[2] - Max number of sub-process, 20 would be better
    # sys.argv[3] - #user to process in each process, 5000 would be better
    if(len(sys.argv)!=5):
        raise StandardError("Usage: python measurement.py total_user_number max_proc_number user_number_per_proc working_dir")
        
    
    g_nUser2Process = int(sys.argv[1])
    if(g_nUser2Process > TOTAL_USER_NUMBER or g_nUser2Process == 0):
        raise StandardError("Error: trying to extrac %d user from all 7,000,000 users" % (g_nUser2Process) )
    g_nUserSelectionBase = math.ceil(float(TOTAL_USER_NUMBER)/float(g_nUser2Process))
    g_nMaxProcessNum = int(sys.argv[2])
    g_nUserPerProcess = int(sys.argv[3])
    strWorkingDir = sys.argv[4] if sys.argv[4].endswith("/") else sys.argv[4]+"/"
   
    # data setup
    strImeisPath = strWorkingDir + "data/distinct_imei.txt"
    strCellLocPath = strWorkingDir + "data/dict.csv"
    strInDir = strWorkingDir + "data/cdr/"
    lsCDR = [\
             "export-userservice-2013090918.dat", \
             "export-userservice-2013090919.dat", \
             "export-userservice-2013090920.dat", \
             "export-userservice-2013090921.dat" \
            ]
    strOutDir = strWorkingDir + "data/out/"

    conductMeasurement(strCellLocPath, strImeisPath, strInDir, lsCDR, strOutDir)
