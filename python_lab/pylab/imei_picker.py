# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 22:11:00 2014

@author: jason
"""

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
                lsFiles.append(dirpath+'\\'+fn)

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
    with open(strOutPath, 'w') as hOutFile:
        for imei in g_dcDistinctIMEI.keys():
            if (pd.isnull(imei)):
                continue
            hOutFile.write("%s\n" % imei.strip())


    return g_dcDistinctIMEI

def getDistinctIMEIsFromFile(strCDR):
    print("--> Scanning file: %s" % strCDR)
    df = pd.read_csv(strCDR, dtype={'imei':object} )
    dc = dict.fromkeys(df['imei'])
    del df
    return dc

if __name__ == '__main__':
    getDistinctIMEIs(None, "D:\\playground\\distinct_imei_full.txt", ["D:\\playground\\export-userservice-2013100310-sample-lite.csv",])
#    dc = getDistinctIMEIs("d:\\playground\\export-userservice-2013100310-sample-lite.csv")
