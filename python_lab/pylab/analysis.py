# -*- coding: utf-8 -*-
'''
Created on 2014年4月4日

@author: yanglin

This module is the main entry for all analysis

'''
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
        dfUserTraffic, dcHeavyUserPaths = heavy_user.findHeavyUser(dcTotalPaths, 10000)
        
        # basic mobility
        input = raw_input("basic mobility? [y/n]>> ")
        if('y' == input.strip() ):
            import basic_mobility
            basic_mobility.execute(dcHeavyUserPaths)
            plt.show()
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

