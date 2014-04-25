# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: yanglin

Main entry for all analysis in one
'''

import data_loader
import app_usage
import basic_mobility
from common_function import *

import matplotlib.pyplot as plt
import sys


if __name__ == '__main__':
    '''
        sys.argv[1] - dir of serialized paths
        sys.argv[2] - path of cell_loc_dict
        sys.argv[3] - 1 means save the raw dcPaths in memory
        sys.argv[4] - #Top App when cleaning data
         
    '''
    
    # input checking
    if (len(sys.argv) != 5):
        raise MyError("Usage: %run analysis.py strSerPathDir strCellLocPath bRaw nTopApp")
    
    strSerPathDir = sys.argv[1]
    strCellLocPath = sys.argv[2]
    bRaw = True if (1 == int(sys.argv[3]) ) else False
    nTopApp = int(sys.argv[4])
    
    # load data
    dcTotoalPaths, sAppUserNum, dfAggCleaned, dcCellLocDict = \
      data_loader.execute(strSerPathDir, strCellLocPath, bRaw, nTopApp)
    
    print("data_loader is finished")
    
    # app usage
    app_usage.execute(sAppUserNum, dfAggCleaned)
    plt.show()
    print("app_usage is finished")
    
    # basic mobility
    basic_mobility.execute(dcTotoalPaths)
    plt.show()
    print("basic_mobility is finished")
    
#     # local App
#     print("Start to analyse local apps...")
#     dcLocalApp = localApp(dfAgg, dcCellLocDict, True)
#     print("-->Total %d apps, %d are local." % (len(dfAgg.index), len(dcLocalApp)) )

