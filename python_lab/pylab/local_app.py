# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450
'''
from common_function import *

def localApp(dfAgg, dcCellLocationDict, bDrawCDF=True):
    '''
        calculate the traffic cdf of cell for all apps,
        and find out those local apps(80% traffic is generated in top 100 cells)
        return serviceType of local app
        
        dfAgg: row=serviceType, column=cell_id
    '''
    # find local App
    dcLocalApps = {}
    for nServiceType in dfAgg.index:
        sAppSorted = dfAgg.loc[nServiceType].order(ascending=False)
        sAppCDF = sAppSorted.cumsum() / sAppSorted.sum()
        if(sAppCDF.iloc[10] >= 0.8): # use top10 CDF as rank critearia
            lsTopCells = []
            for cid in sAppSorted.index[:10]:
                loc = dcCellLocationDict.get(cid, (0.0, 0.0))
                attribute = sAppSorted.loc[cid]
                tp = (cid, loc, attribute)
                lsTopCells.append(tp)
            dcLocalApps[nServiceType]=lsTopCells
            
    return dcLocalApps

import sys
if __name__ == '__main__':
    pass