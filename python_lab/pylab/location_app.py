# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450
'''
from common_function import *
import region_type

def getLocalApps(dfAgg, dcCellLoc):
    '''
        Find out those local apps whose 80% traffic is generated in top 10 cells
        
        Params:       
                dfAgg     - row=serviceType, column=cell_id
                dcCellLoc - dict of cell & location
                
        Return:
                a dict like {serviceType: list[(lac-cid, (lat, long), traffic)...], }
    '''
    # find local App
    dcLocalApps = {}
    for nServiceType in dfAgg.index:
        sAppSorted = dfAgg.loc[nServiceType].order(ascending=False)
        sAppCDF = sAppSorted.cumsum() / sAppSorted.sum()
        if(sAppCDF.iloc[20] >= 0.8): # use top20 CDF as rank critearia
            lsTopCells = []
            for cid in sAppSorted.index[:10]:
                loc = dcCellLoc.get(cid, (0.0, 0.0))
                attribute = sAppSorted.loc[cid]
                tp = (cid, loc, attribute)
                lsTopCells.append(tp)
            dcLocalApps[nServiceType]=lsTopCells
            
    return dcLocalApps
    
def getLocalAppRegionType(dcLocalApps, dfCellLocType):
    pass
