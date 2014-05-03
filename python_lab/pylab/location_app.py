# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450
'''
from common_function import *
import region_type
import app_category

def getLocalApps(dfAgg, dfCellLocType):
    '''
        Find out those local apps whose 80% traffic is generated in top 10 cells
        
        Params:       
                dfAgg         - row=serviceType, column=cell_id
                dfCellLocType - dataframe of cell & location & typeID
                
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
                dLat = dfCellLocType.loc[cid]['lat']
                dLong = dfCellLocType.loc[cid]['long']
                nTypeID = dfCellLocType.loc[cid]['typeID']
                attribute = sAppSorted.loc[cid]
                tp = (cid, dLat, dLong, nTypeID, attribute)
                lsTopCells.append(tp)
            dcLocalApps[nServiceType]=lsTopCells
            
    return dcLocalApps
    
def getCategoryDistributionOnRegions(dfAppUserNumInCells, dfAppTrafficInCells, dfCellLocType):
    '''
        get user & traffic distribution of regions for each app category
        
        Params:
                dfAppUserNumInCells - row=serviceType, column='lac-cid'
                dfAppTrafficInCells - row=serviceType, column='lac-cid'
                
        Return:
                dfCategoryUserInRegions    - row = categoryName, column = region_type_name
                dfCategoryTrafficInRegions - row = categoryName, column = region_type_name
    '''
    dfCategoryUserInRegions = pd.DataFrame()
    dfCategoryTrafficInRegions = pd.DataFrame()
    
    # divide by category
    dfCategoryUserInCells = pd.DataFrame()
    dfCategoryTrafficInCells = pd.DataFrame()
    for tp in app_category.g_dcCategory.items():
        dfCategoryUserInCells[tp[0]] = dfAppUserNumInCells.loc[dfAppUserNumInCells.index.isin(tp[1])].sum(axis=0)
        dfCategoryTrafficInCells[tp[0]] = dfAppTrafficInCells.loc[dfAppTrafficInCells.index.isin(tp[1])].sum(axis=0)
    
    for tp in region_type.g_dcRegionTypeName.items():
        dfCategoryUserInRegions[tp[1]] = (dfCategoryUserInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
        dfCategoryTrafficInRegions[tp[1]] = (dfCategoryTrafficInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
        
    return dfCategoryUserInCells, dfCategoryTrafficInCells, dfCategoryUserInRegions, dfCategoryTrafficInRegions

        