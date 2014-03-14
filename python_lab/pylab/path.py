# -*- coding: utf-8 -*-
'''
Created on 2014年3月14日

@author: jason
'''

from common_function import *

class CPath(object):
    '''
    a roaming path for each user
    '''


    def __init__(self, strIMEI):
        '''
        Constructor
        '''
        self.m_strIMEI = strIMEI
        
        # moving speed
        self.m_dAvgSpeed = 0.0
        self.m_dMaxSpeed = 0.0
        self.m_dMinSpeed = 0.0
        
        # distance
        self.m_nCellNum = 0
        self.m_nDistance = 0.0
        
        # time
        self.m_startTime = 0
        self.m_endTime = 0
        
        # traffic
        self.m_nTotalUpBytes = 0
        self.m_nTotalDownBytes = 0
        
        self.m_lsNodes = []
        
    def updatePathInfo(self):
        '''
        re-calculate path info
        '''
        dLastLat = 0.0
        dLastLong = 0.0
        
        for node in self.m_lsNodes:
            # moving speed
            self.m_dAvgSpeed += node.m_dSpeed
            self.m_dMaxSpeed = max(self.m_dMaxSpeed, node.m_dSpeed)
            if (self.m_dMinSpeed == 0.0):
                self.m_dMinSpeed = node.m_dSpeed
            elif (node.m_dSpeed != 0.0):
                self.m_dMinSpeed = min(self.m_dMinSpeed, node.dSpeed)
            
            # distance
            self.m_nCellNum = len(self.m_lsNodes)
            if (node.m_dLat!=0.0 and node.m_dLong!=0.0):
                if(dLastLat!=0.0 and dLastLong!=0.0):
                    self.m_nDistance += calculateDistance(dLastLat, dLastLong, node.m_dLat, node.m_dLong)
                    
                dLastLat = node.dLat
                dLastLong = node.dLastLong
                
            # traffic
            for app in node.m_lsApps:
                self.m_nTotalUpBytes += app.nUpBytes
                self.m_nTotalDownBytes += app.nDownBytes
        
        self.m_dAvgSpeed = self.m_dAvgSpeed/len(self.m_lsNodes)
        
        # time
        if(len(self.m_lsNodes) >=1 ):
            self.m_startTime = self.m_lsNodes[0].m_startTime
            self.m_endTime = self.m_lsNodes[-1].m_endTime
            
            
        
        