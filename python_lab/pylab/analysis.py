# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450

Main entry for all analysis in one
'''
from data_loader import *
from local_app import *
from common_function import *

import sys
if __name__ == '__main__':
    
    # input checking
    if (len(sys.argv) != 4):
        raise MyError("Usage: %run analysis.py serialized_path cell_loc_dict_path outdir")
    
    # load data
    print("Start to deserialize from file...") 
    dcPaths = deserializeFromFile(sys.argv[1])
     
    print("Start to aggregate data by m_nDownBytes...")
    dcAggregated = aggregateData(dcPaths)
    
    print("Start to get user number...")
    dcAggregatedAppUserNum = AggregateAppUserNum(dcPaths)
     
    print("Start to clean data...")
    cleanData(dcAggregated, dcAggregatedAppUserNum)
    
    print("Start to construct cell-location dict...")
    dcCellLocDict = constructCellLocDict(sys.argv[2])
    
    dfAgg = pd.DataFrame(dcAggregated)
    print("data_loader is ready----")
    
    # local App
    print("Start to analyse local apps...")
    dcLocalApp = localApp(dfAgg, dcCellLocDict, True)
    print("-->Total %d apps, %d are local." % (len(dfAgg.index), len(dcLocalApp)) )
    
    print("Start to output local apps...")
