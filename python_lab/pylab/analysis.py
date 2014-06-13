# -*- coding: utf-8 -*-
'''
This module is the main entry for all analysis

@author: yanglin
'''

from common_function import *

import matplotlib.pyplot as plt
import sys

def execute(strSerPathDir, strCellLocPath, bRaw, nTopApp, dcTotalPaths):
    
    # load data
    input = raw_input("load data? [y/n]>> ")
    if('y' == input.strip() ):
        import data_loader
        dcTotalPaths, sAppUserNum, dfAggCleaned, dcCellLocDict = \
          data_loader.execute(strSerPathDir, strCellLocPath, bRaw, nTopApp)
        print("data_loader is finished")
    
    # basic app usage
    input = raw_input("basic app usage? [y/n]>> ")
    if('y' == input.strip() ):
        import app_usage
        app_usage.execute(sAppUserNum, dfAggCleaned)
        plt.show()
        print("app_usage is finished")
    
    # basic mobility
    input = raw_input("basic mobility? [y/n]>> ")
    if('y' == input.strip() ):
        import basic_mobility
        basic_mobility.execute(dcTotalPaths)
        plt.show()
        print("basic_mobility is finished")
    
    # mobility & App usage
    input = raw_input("mobility_app? [y/n]>> ")
    if('y' == input.strip() ):
        import mobility_app
        mobility_app.execute(dcTotalPaths)
        plt.show()
        print("mobility_app is finished")
    
    # location & app usage
    input = raw_input("location_app? [y/n]>> ")
    if('y' == input.strip() ):
        import location_app
        dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
        dfSimilarity = location_app.execute(dcTotalPaths, dfCellLocType)
        plt.show()
        print("location_app is finished")
        
    # ---- Heavy traffic users ----
    input = raw_input("heavy traffic users ? [y/n]>> ")
    if('y' == input.strip() ):
        import path_selector
        dfUserTraffic, dcHeavyUserPaths, dcNormalUserPaths = path_selector.selectPathByTraffic(dcTotalPaths, 400000)
        
        # basic mobility
        input = raw_input("basic mobility? [y/n]>> ")
        if('y' == input.strip() ):
            import basic_mobility
            
            fig, axes = plt.subplots(nrows=1, ncols=3)
            
            sMobilityCellHeavy, sMobilitySpeedHeavy, sMobilityRogHeavy = \
                basic_mobility.getMobilityDistribution(dcHeavyUserPaths)
            sMobilityCellNormal, sMobilitySpeedNormal, sMobilityRogNormal = \
                basic_mobility.getMobilityDistribution(dcNormalUserPaths)
                
            basic_mobility.drawCDFofMobility(sMobilityCellHeavy, sMobilitySpeedHeavy, sMobilityRogHeavy,\
                                             axes=axes, strLable='heavy subscriber', bDraw=False)
            basic_mobility.drawCDFofMobility(sMobilityCellNormal, sMobilitySpeedNormal, sMobilityRogNormal,\
                                             axes=axes, strLable='normal subscriber', bDraw=True)
            print("basic_mobility is finished")
        
        # mobility & usage
        input = raw_input("mobility_app? [y/n]>> ")
        if('y' == input.strip() ):
            import mobility_app
            
            print("heavy subscriber")
            mobility_app.execute(dcHeavyUserPaths)
            plt.show()
            
            print("normal subscriber")
            mobility_app.execute(dcNormalUserPaths)
            plt.show()
            print("mobility_app is finished")
    
        # location & App usage
        input = raw_input("location_app ? [y/n]>> ")
        if('y' == input.strip() ):
            import location_app
            dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
            
            print("heavy subscriber")
            dfSimilarity = location_app.execute(dcHeavyUserPaths, dfCellLocType)
            plt.show()
            
            print("normal subscriber")
            dfSimilarity = location_app.execute(dcNormalUserPaths, dfCellLocType)
            plt.show()
            print("location_app is finished")
        
    # ---- Heavy mobile users ----
    input = raw_input("heavy mobile users ? [y/n]>> ")
    if('y' == input.strip() ):
        import path_selector
        dfUserMobility, dcHeavyUserPaths, dcNormalUserPaths = path_selector.selectPathByMobility(dcTotalPaths, 400000)
        
        # basic app usage
        input = raw_input("basic app usage? [y/n]>>")
        if ('y' == input.strip() ):
            import app_usage
            app_usage.execute(dcPaths=dcHeavyUserPaths, strAttribName='m_nDownBytes')
            
        # location & App usage
        input = raw_input("location_app ? [y/n]>> ")
        if('y' == input.strip() ):
            import location_app
            dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
            
            print("heavy subscriber")
            dfSimilarity = location_app.execute(dcHeavyUserPaths, dfCellLocType)
            plt.show()
            
            print("normal subscriber")
            dfSimilarity = location_app.execute(dcNormalUserPaths, dfCellLocType)
            plt.show()
            print("location_app is finished")
        
    
    #---- 2G vs. 3G ----
    input = raw_input("2G vs. 3G ? [y/n]>> ")
    if('y' == input.strip() ):
        import path_selector
        dc2G, dc3G = path_selector.selectPathByNetwork(dcTotalPaths)
        
        # basic mobility
        input = raw_input("basic mobility? [y/n]>> ")
        if('y' == input.strip() ):
            import basic_mobility
            
            fig, axes = plt.subplots(nrows=1, ncols=3)
            sMobilityCell2G, sMobilitySpeed2G, sMobilityRog2G = \
                basic_mobility.getMobilityDistribution(dc2G)
            sMobilityCell3G, sMobilitySpeed3G, sMobilityRog3G = \
                basic_mobility.getMobilityDistribution(dc3G)
                
            basic_mobility.drawCDFofMobility(sMobilityCell2G, sMobilitySpeed2G, sMobilityRog2G,\
                                             axes=axes, strLable='2.5G subscriber', bDraw=False)
            basic_mobility.drawCDFofMobility(sMobilityCell3G, sMobilitySpeed3G, sMobilityRog3G,\
                                             axes=axes, strLable='3G subscriber', bDraw=True)
            print("basic_mobility is finished")
        
        
        # mobility & usage
        input = raw_input("mobility_app? [y/n]>> ")
        if('y' == input.strip() ):
            import mobility_app
            
            print("2G subscriber")
            mobility_app.execute(dc2G)
            plt.show()
            
            print("3G subscriber")
            mobility_app.execute(dc3G)
            plt.show()
            
            print("mobility_app is finished")
    
        # location & App usage
        input = raw_input("location_app ? [y/n]>> ")
        if('y' == input.strip() ):
            import location_app
            
            dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
            
            print("2G subscriber")
            dfSimilarity = location_app.execute(dc2G, dfCellLocType)
            plt.show()
            
            print("3G subscriber")
            dfSimilarity = location_app.execute(dc3G, dfCellLocType)
            plt.show()
            
            print("location_app is finished")


    print("====All the analysis is finished====")

