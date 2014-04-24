# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *
import pandas as pd

import os

 
def constructCellLocFromAdditionalSource(strPath):
    dcNew = {}
    with open(strPath) as hNew:
        for line in hNew:
            lsItems = line.split(',')
            if(len(lsItems) != 8 or False == lsItems[0].isdigit() ):
                continue
            strKey = "%s-%s" % (lsItems[0].strip(), lsItems[1].strip())
            loc = (0., 0.)
            try:
                if( lsItems[2] != '' and lsItems[3] != '' ):
                    loc=(float(lsItems[2]), float(lsItems[3]) )
            except ValueError as v:
                print("==>%s, %s" % (lsItems[2], lsItems[3]))
            dcNew[strKey] = loc

    return dcNew

  
def findDiff(dfPrevious, dcNew):
    lsDis = []
    for tp in dfPrevious.itertuples():
        key = tp[0]
        dLat = float(tp[1])
        dLong = float(tp[2])
        
        newLoc = dcNew.get(key, (0., 0.) )
        
        if(newLoc != (0., 0.) and dLat != 0. and dLong != 0.):
            dis = calculateDistance(dLat, dLong, newLoc[0], newLoc[1])
            lsDis.append(dis)
        
    sDis = pd.Series(lsDis)
    sDis.describe()
    return sDis

def ensurePathExist(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if __name__ == '__main__':
    ensure_dir(".\\dd\\ss74\\test.txt")
