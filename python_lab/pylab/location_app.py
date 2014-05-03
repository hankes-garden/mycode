# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: y00752450
'''
from common_function import *
import region_type
import app_category

import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib

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
                dfCategoryUserInCells      - row = 'lac-cid', column = category_name
                dfCategoryTrafficInCells   - row = 'lac-cid', column = category_name 
                dfCategoryUserInRegions    - row = category_name, column = region_type_name
                dfCategoryTrafficInRegions - row = category_name, column = region_type_name
    '''
    
    
    # group by category
    dfCategoryUserInCells = pd.DataFrame(index=dfAppUserNumInCells.columns)
    dfCategoryTrafficInCells = pd.DataFrame(index=dfAppTrafficInCells.columns)
    for tp in app_category.g_dcCategory.items():
        dfCategoryUserInCells[tp[0]] = dfAppUserNumInCells.loc[dfAppUserNumInCells.index.isin(tp[1])].sum(axis=0)
        dfCategoryTrafficInCells[tp[0]] = dfAppTrafficInCells.loc[dfAppTrafficInCells.index.isin(tp[1])].sum(axis=0)
    
    # group by region type
    dfCategoryUserInRegions = pd.DataFrame(index=app_category.g_dcCategory.keys())
    dfCategoryTrafficInRegions = pd.DataFrame(index=app_category.g_dcCategory.keys())
    for tp in region_type.g_dcRegionTypeName.items():
        dfCategoryUserInRegions[tp[1]] = \
          (dfCategoryUserInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
        dfCategoryTrafficInRegions[tp[1]] = \
          (dfCategoryTrafficInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
        
    return dfCategoryUserInCells, dfCategoryTrafficInCells, dfCategoryUserInRegions, dfCategoryTrafficInRegions

def drawCategoryAccessProbabilityInRegions(dfCategoryUserInRegions):
    '''
        get access probability distribution of regions for each app categories
        
        Params:
                dfCategoryUserInRegions - row = category_name, column = region_type_name
    '''
    dfUserBaseInRegions = pd.DataFrame(index = dfCategoryUserInRegions.columns)
    
    for cate in dfCategoryUserInRegions.index:
        dfUserBaseInRegions[cate] = dfCategoryUserInRegions.sum(axis=0)
        
    dfCategoryAccProb = dfCategoryUserInRegions.T.div(dfUserBaseInRegions)
    
    ax0 = plt.figure().add_subplot(111)
    
    # color
    nColorCount = len(dfCategoryUserInRegions.index)

    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    ax0.set_color_cycle([scalarMap.to_rgba(i) for i in range(nColorCount)])
    
    # plot
    dfCategoryAccProb.plot(ax=ax0, kind='bar', legend=False)
    ax0.set_ylabel = 'access probability (%)'
    
    # hatches
    pred = lambda obj: isinstance(obj, matplotlib.patches.Rectangle)
    bars = filter(pred, ax0.get_children())
    hatches = ''.join(h*len(dfCategoryAccProb) for h in '/\\|-+xoO.*')

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax0.legend(loc='upper right', bbox_to_anchor=(1, 1), ncol=4)
    
    plt.show()
    
def drawCategoryPerCapitaTrafficInRegions(dfCategoryUserInRegions, dfCategoryTrafficInRegions):
    '''
        get access probability distribution of regions for each app categories
        
        Params:
                dfCategoryUserInRegions - row = category_name, column = region_type_name
    '''
    dfCategoryPerCapitaTrafficInRegions = dfCategoryTrafficInRegions.T.div(dfCategoryUserInRegions.T)
    
    ax0 = plt.figure().add_subplot(111)
    dfCategoryPerCapitaTrafficInRegions.plot(ax=ax0, kind='bar')
    ax0.set_ylabel = 'per capita traffic'
    ax0.legend(loc='upper right')
    
    plt.show()
    