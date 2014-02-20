# -*- coding: utf-8 -*-
'''
Created on 2014年2月16日

@author: lyangab
'''

class CAppState(object):
    '''
    statistical info of an application 
    '''


    def __init__(self, nServiceType, nServiceGroup):
        '''
        Constructor
        '''
        self.m_nServiceType = nServiceType
        self.m_nServiceGroup = nServiceGroup
        
        self.m_nUserNum = 1    # How many users used this application
        self.m_nCellNum = 0.0  # for now, it's the number of cells, in which this application has been used
        
#       uplink
        self.m_nAvgUpBytes = 0 # the average traffic generated(may generated in several cells )
        self.m_nMaxUpBytes = 0
        self.m_nMinUpBytes = 99999999999999999999
        
        self.m_dAvgUpSpeed = 0.0 # the average speed experienced in each session(only in one cell)
        self.m_dMaxUpSpeed = 0.0
        self.m_dMinUpSpeed = 99999999999999999999.9
        
#       downlink
        self.m_nAvgDownBytes = 0
        self.m_nMaxDownBytes = 0
        self.m_nMinDownBytes = 99999999999999999999
        
        self.m_dAvgDownSpeed = 0.0
        self.m_dMaxDownSpeed = 0.0
        self.m_dMinDownSpeed = 99999999999999999999.9
    
    def toString(self):
        text = "%d,%d,%d,%d,%d,%d,%d,%.2f,%.2f,%.2f,%d,%d,%d,%.2f,%.2f,%.2f" % \
        (self.m_nServiceType, self.m_nServiceGroup, \
         self.m_nUserNum, self.m_nCellNum,\
         self.m_nAvgUpBytes, self.m_nMaxUpBytes,\
         self.m_nMinUpBytes, self.m_dAvgUpSpeed,\
         self.m_dMaxUpSpeed, self.m_dMinUpSpeed, \
         self.m_nAvgDownBytes, self.m_nMaxDownBytes,\
         self.m_nMinDownBytes, self.m_dAvgDownSpeed, \
         self.m_dMaxDownSpeed, self.m_dMinDownSpeed)
        
        return text
        