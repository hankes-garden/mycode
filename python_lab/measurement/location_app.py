# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

This module analyze the relationship btw app usage and location

@author: y00752450
'''
from common_function import *

import region_type
import app_category
import basic_location

import math
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib

def findLocalApps(dfAgg, dfCellLocType):
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

def getCategoryDistributionInRegions(dcPaths, dfCellLocType):
    '''
        This function computes:
            1. total user number in different types of locations;
            2. category user number in different types of locations;
            3. category traffic in different types of locations; 
            
        param:
                dcPaths       - roaming paths
                dfCellLocType - index=lac-cid
        return:
               srUserNumPerRegion         - total user number per region, index:region
               dfCategoryUserNumPerRegion - category user number per region, row:category, col:region
               dfCategoryTrafficPerRegion - category traffic per region, row:category, col:region
    '''
    
    dcTotalUserNumPerRegion = {}             # total user number in different types of locations;
    dcCategoryUserNumPerRegion = {}          # category user number in different types of locations;
    dcCategoryTrafficPerRegion = {}          # category traffic in different types of locations;
    
    for path in dcPaths.values():
        for node in path.m_lsNodes:
            strKey = "%d-%d" % (node.m_nLac, node.m_nCellID)
            nRegionType = dfCellLocType.loc[strKey]["typeID"]
            strRegionName = region_type.g_dcRegionTypeName[nRegionType]
            
            # total user
            updateDictBySum(dcTotalUserNumPerRegion, strRegionName, 1)
            
            
            dcCategoryUserNumForCurrentRegion = dcCategoryUserNumPerRegion.get(strRegionName, None)
            if (dcCategoryUserNumForCurrentRegion is None):
                dcCategoryUserNumForCurrentRegion = {}
                dcCategoryUserNumPerRegion[strRegionName] = dcCategoryUserNumForCurrentRegion
                
            dcCategoryTrafficForCurrentRegion = dcCategoryTrafficPerRegion.get(strRegionName, None)
            if (dcCategoryTrafficForCurrentRegion is None):
                dcCategoryTrafficForCurrentRegion = {}
                dcCategoryTrafficPerRegion[strRegionName] = dcCategoryTrafficForCurrentRegion
                
            dcCategoryUserNumForCurretNode = {} 
            for app in node.m_lsApps:
                strCategoryName = app_category.getAppCategory(app.m_nServiceType)
                dcCategoryUserNumForCurretNode[strCategoryName] = 1
                
                updateDictBySum(dcCategoryTrafficForCurrentRegion, strCategoryName, app.m_nDownBytes)
                
                
            for (k,v) in dcCategoryUserNumForCurretNode.iteritems():
                updateDictBySum(dcCategoryUserNumForCurrentRegion, k, v)
                
    srUserNumPerRegion = pd.Series(dcTotalUserNumPerRegion)
    dfCategoryUserNumPerRegion = pd.DataFrame(dcCategoryUserNumPerRegion)
    dfCategoryTrafficPerRegion = pd.DataFrame(dcCategoryTrafficPerRegion)
    
    # delete unknown category
    dfCategoryUserNumPerRegion.drop(labels=app_category.g_strUnknown, inplace=True)
    dfCategoryTrafficPerRegion.drop(labels=app_category.g_strUnknown, inplace=True)
    
    return srUserNumPerRegion, dfCategoryUserNumPerRegion, dfCategoryTrafficPerRegion
                
            
    
# def _getCategoryDistributionInRegions(dfAppUserNumInCells, dfAppTrafficInCells, dfCellLocType):
#     '''
#         get user & traffic distribution of regions for each app category
#         
#         Params:
#                 dfAppUserNumInCells - row=serviceType, column='lac-cid'
#                 dfAppTrafficInCells - row=serviceType, column='lac-cid'
#                 
#         Return:
#                 dfCategoryUserInCells      - row = 'lac-cid', column = category_name
#                 dfCategoryTrafficInCells   - row = 'lac-cid', column = category_name 
#                 dfCategoryUserInRegions    - row = category_name, column = region_type_name
#                 dfCategoryTrafficInRegions - row = category_name, column = region_type_name
#     '''
#     # group by category
#     dfCategoryUserInCells = pd.DataFrame(index=dfAppUserNumInCells.columns)
#     dfCategoryTrafficInCells = pd.DataFrame(index=dfAppTrafficInCells.columns)
#     for tp in app_category.g_dcCategory.items():
#         dfCategoryUserInCells[tp[0]] = dfAppUserNumInCells.loc[dfAppUserNumInCells.index.isin(tp[1])].sum(axis=0)
#         dfCategoryTrafficInCells[tp[0]] = dfAppTrafficInCells.loc[dfAppTrafficInCells.index.isin(tp[1])].sum(axis=0)
#     
#     # group by region type
#     dfCategoryUserInRegions = pd.DataFrame(index=app_category.g_dcCategory.keys())
#     dfCategoryTrafficInRegions = pd.DataFrame(index=app_category.g_dcCategory.keys())
#     for tp in region_type.g_dcRegionTypeName.items():
#         dfCategoryUserInRegions[tp[1]] = \
#           (dfCategoryUserInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
#         dfCategoryTrafficInRegions[tp[1]] = \
#           (dfCategoryTrafficInCells.loc[dfCellLocType[dfCellLocType['typeID']==tp[0]].index]).sum(axis=0)
#         
#     return dfCategoryUserInCells, dfCategoryTrafficInCells, dfCategoryUserInRegions, dfCategoryTrafficInRegions

def drawCategoryAccessProbabilityInRegions(dfCategoryUserNumPerRegion, srUserNumPerRegion):
    '''
        get access probability distribution of regions for each app categories
        
        Params:
                dfCategoryUserInRegions - row = category_name, column = region_type_name
    '''
    # calculate access probability
    dfCategoryAccProb = dfCategoryUserNumPerRegion.div(srUserNumPerRegion, axis=1)
    
    # prepare to draw
    ax0 = plt.figure().add_subplot(111)
    
    # color
    nColorCount = len(dfCategoryUserNumPerRegion.index)

    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    # plot
    dfCategoryAccProb.T.plot(ax=ax0, kind='bar', legend=False, \
                           color=[scalarMap.to_rgba(i) for i in range(nColorCount)], ylim=(0., 0.8))
    ax0.set_ylabel = 'access probability (%)'
    ax0.set_xticklabels(dfCategoryAccProb.columns.tolist(), rotation=0)
    
    # hatches
    pred = lambda obj: isinstance(obj, matplotlib.patches.Rectangle)
    bars = filter(pred, ax0.get_children())
    hatches = ''.join(h*len(dfCategoryAccProb) for h in '|oO/\\-x.*+')

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    ax0.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0), ncol=1)
    
    plt.show()
    
def drawCategoryPerCapitaTrafficInRegions(dfCategoryUserInRegions, srUserNumPerRegion):
    '''
        get access probability distribution of regions for each app categories
        
        Params:
                dfCategoryUserInRegions - row = category_name, column = region_type_name
    '''
    dfCategoryPerCapitaTrafficInRegions = dfCategoryUserInRegions.sum(axis=0).div(srUserNumPerRegion, axis=1)
    
    # prepare to draw
    ax0 = plt.figure().add_subplot(111)
    
    # color
    nColorCount = len(dfCategoryUserInRegions.index)
    cm = plt.get_cmap('gist_rainbow')
    cNorm  = colors.Normalize(vmin=0, vmax=nColorCount-1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    
    dfCategoryPerCapitaTrafficInRegions.T.plot(ax=ax0, kind='bar', \
                                             color=[scalarMap.to_rgba(i) for i in range(nColorCount)])
    ax0.set_ylabel = 'per capita traffic'
    ax0.set_xticklabels(dfCategoryPerCapitaTrafficInRegions.columns.tolist(), rotation=0)
    
    # hatches
    pred = lambda obj: isinstance(obj, matplotlib.patches.Rectangle)
    bars = filter(pred, ax0.get_children())
    hatches = ''.join(h*len(dfCategoryPerCapitaTrafficInRegions) for h in '|oO/\\-x.*+')

    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    
    ax0.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0), ncol=1)
    
    plt.show()
    
def drawTotoalDistribution(dfAppUserNumInCells, dfAppTrafficInCells):
    '''
        
    '''
    fig, axes = plt.subplots(nrows=1, ncols=2)
    
    sAppUser = dfAppUserNumInCells.sum(axis=1)
    sAppTraffic = dfAppTrafficInCells.sum(axis=1) / 1024.0
    
    sAppUser.order(ascending=False)[:200].plot(ax=axes[0], kind='bar', use_index=False, logy=True)
    sAppTraffic.order(ascending=False)[:200].plot(ax=axes[1], kind='bar', use_index=False, logy=True)
    
    axes[0].set_yscale('log')
    axes[0].set_xlabel('distribution of users')
    axes[0].set_ylabel('# users')
    
    axes[1].set_yscale('log')
    axes[1].set_xlabel('distribution of traffic volume')
    axes[1].set_ylabel('traffic volume (KB)')
    
    plt.show()
    
def calculateSimiliarity(sCell1, sCell2):
    '''
        calculate the Euclidean distance and use it as a similarity metrics
    '''
    dDis = math.sqrt( (sCell1-sCell2).pow(2).sum() )
    return dDis
    
def CalculateAppUsageSimilarityAmongCells(dfAppUserNumInCells, dfAppTrafficInCells, dfCellLocType):
    '''
        Calculate the correlation of App usage among locations of same type
        
        Params:
                dfAppUserNumInCells - row=serviceType, column='lac-cid'
                dfAppTrafficInCells - row=serviceType, column='lac-cid'
                
        return:
                dfSimilarity - row = cell_id*cell_id, columns=['same_type','distance', 'similarity']
    '''
    dfPerCapitaTraffic = dfAppTrafficInCells.div(dfAppUserNumInCells)
    
    # select cells whose type is known
    lsKnownCells = dfCellLocType[dfCellLocType['typeID'] != region_type.ID_TYPE_UNKNOWN ].index.tolist()
    dfPerCapitaTrafficInKnownCell = dfPerCapitaTraffic.loc[:, lsKnownCells]
    
    
    lsData = []
    for i in range(0, len(dfPerCapitaTrafficInKnownCell.columns)-1):
        sTarget = dfPerCapitaTrafficInKnownCell.iloc[:,i]
        for j in range(i+1, len(dfPerCapitaTrafficInKnownCell.columns)-1):
            sCompare = dfPerCapitaTrafficInKnownCell.iloc[:,j]
            
            # get location information
            sTargetLoc = 0   # location information of targe cell
            sCompareLoc = 0  # location information of targe cell
            try:
                sTargetLoc = dfCellLocType.loc[sTarget.name]
                sCompareLoc = dfCellLocType.loc[sCompare.name]
            except KeyError:
                continue
            
            # if the type of both cells are known, then calculate the similarity
            if(sTargetLoc['typeID'] != region_type.ID_TYPE_UNKNOWN 
               and sCompareLoc['typeID'] != region_type.ID_TYPE_UNKNOWN):
                strID = "%s*%s" % (sTarget.name, sCompare.name)
                dSimilarity = calculateSimiliarity(sTarget, sCompare)
                nSameType = 1 if sTargetLoc['typeID'] == sCompareLoc['typeID'] else 0
                dDistance = calculateDistance(sTargetLoc['lat'], sTargetLoc['long'], sCompareLoc['lat'], sCompareLoc['long'])
                dcTemp = {'cid*cid':strID, 'same_type': nSameType, 'distance': dDistance, 'similarity':dSimilarity}
                lsData.append(dcTemp)
                
    dfSimilarity = pd.DataFrame(lsData)
    dfSimilarity.set_index(keys='cid*cid', inplace=True)
    return dfSimilarity
    
    
def execute(dcPaths, dfCellLocType):
    '''
        1. access probability of each app category vs. location
        2. per capita traffic of each app category vs. location
        3. app traffic similarity btw cells vs. distance & location types [disabled by default] 
    '''
    
    # get category user and traffic distribution
    srTotalUserNumPerRegion, dfCategoryUserNumPerRegion, dfCategoryTrafficPerRegion = \
        getCategoryDistributionInRegions(dcPaths, dfCellLocType)
    
    # draw
    drawCategoryAccessProbabilityInRegions(dfCategoryUserNumPerRegion, srTotalUserNumPerRegion)
    drawCategoryPerCapitaTrafficInRegions(dfCategoryTrafficPerRegion, srTotalUserNumPerRegion)
    
    return None
    