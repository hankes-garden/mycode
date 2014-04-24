# -*- coding: utf-8 -*-
'''
Created on 2014年4月24日

@author: jason
'''

from common_function import *

import pandas as pd
import matplotlib.pyplot as plt

def getMobility(dcPaths, kind='cell_num'):
    pass
    

def drawCDFofMobility(sUserMobilityCell, sUserMobilitySpeed, sUserMobilityRog):
    '''
        draw user CDF of mobility
    '''
    fig, axes = plt.subplots(nrows=1, ncols=3)
    
    # CDF of mobility by cell_num
    sCDFCell = sUserMobilityCell.order(ascending=False).cumsum()/sUserMobilityCell.sum()
    sCDFCell.plot(ax=axes[0], style='-o')
    
    # CDF of mobility by cell_num
    sCDFSpeed = sUserMobilitySpeed.order(ascending=False).cumsum()/sUserMobilitySpeed.sum()
    sCDFSpeed.plot(ax=axes[1], style='-o')
    
    # CDF of mobility by cell_num
    sCDFRog = sUserMobilityRog.order(ascending=False).cumsum()/sUserMobilityRog.sum()
    sCDFRog.plot(ax=axes[2], style='-o')
    
    # set style
    axes[0].set_xlabel('# cells')
    axes[0].set_ylabel('CDF(%)')
    
    axes[1].set_xlabel('speed level')
    axes[1].set_ylabel('CDF(%)')
    
    axes[2].set_xlabel('radius of gyration')
    axes[2].set_ylabel('CDF(%)')
        

if __name__ == '__main__':
    pass