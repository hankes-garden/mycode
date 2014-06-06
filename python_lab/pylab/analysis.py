# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: yanglin

This module is the main entry for all analysis

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
        
    # Heavy Users
    input = raw_input("heavy users ? [y/n]>> ")
    if('y' == input.strip() ):
        import heavy_user
        dfUserTraffic, dcHeavyUserPaths, dcNormalUserPaths = heavy_user.findHeavyUser(dcTotalPaths, 10000)
        
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
            mobility_app.execute(dcHeavyUserPaths)
            plt.show()
            print("mobility_app is finished")
    
        # location & App usage
        input = raw_input("location_app ? [y/n]>> ")
        if('y' == input.strip() ):
            import location_app
            dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
            dfSimilarity = location_app.execute(dcHeavyUserPaths, dfCellLocType)
            plt.show()
            print("location_app is finished")
        
    # 2G vs. 3G
    input = raw_input("2G vs. 3G ? [y/n]>> ")
    if('y' == input.strip() ):
        import network_type
        dc2G, dc3G = network_type.getNetworks(dcTotalPaths)
        
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
            mobility_app.execute(dc2G)
            plt.show()
            
            mobility_app.execute(dc3G)
            plt.show()
            print("mobility_app is finished")
    
        # location & App usage
        input = raw_input("location_app ? [y/n]>> ")
        if('y' == input.strip() ):
            import location_app
            dfCellLocType = pd.read_csv("../../data/cell_loc_type.txt", index_col='lac-cid')
            dfSimilarity = location_app.execute(dc2G, dfCellLocType)
            plt.show()
            print("location_app is finished")


    print("====All the analysis is finished====")

