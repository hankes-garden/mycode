# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450
'''
import common_statistics as st
import data_loader as dl
from common_function import *

import pandas as pd

def localApp(dfAggregated, bDrawCDF=True):
    '''
        calculate the traffic cdf of cell for all apps,
        and find out those local apps(80% traffic is generated in top 100 cells)
    '''
    # find local App
    lsLocalApps = []
    for strAppName in dfAggregated.index:
        sAppTrafficSorted = dfAggregated.loc[strAppName].order(ascending=False)
        sAppTrafficCDF = sAppTrafficSorted.cumsum() / sAppTrafficSorted.sum()
        if(sAppTrafficCDF.iloc[100] >= 0.8):
            lsLocalApps.append((strAppName, sAppTrafficCDF.iloc[10])) # use top10 CDF as rank critearia
            
    lsLocalApps.sort(key=lambda app:app[1], reverse=True)   
    print("local apps:")
    for app in lsLocalApps:
        print("serviceType = %s" % app[0] )
        
    # slice the top local apps    
    lsLocalAppsSorted = [app[0] for app in lsLocalApps]
    dfLocalApps = dfAggregated.T.ix[:, lsLocalAppsSorted]
        
    return dfLocalApps

import sys
if __name__ == '__main__':
    pass