# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jason
'''
import common_function
import time

class CNode(object):
    '''
    A node in roaming path
    '''


    def __init__(self, strIMEI, nLac, nCellID):
        '''
        Constructor
        '''
        self.m_strIMEI = strIMEI
        self.m_nLac = nLac
        self.m_nCellID = nCellID
        
        self.m_firstTime = time.localtime(0)
        self.m_endTime = time.localtime(0)
        self.m_nRat = 0
        self.m_dDuration = 0
        self.m_dMobility_speed = 0.0
        self.m_lsApps = list() # here is an empty list
        
    def findAppIndex(self, app):
        index = -1
        for i in self.m_lsApps:
            if i.m_nServiceType == app.m_nServiceType:
                index = self.m_lsApps.index(i)
        
        return index
    
    def updateDuration(self):
        self.m_dDuration = time.mktime(self.m_endTime) - time.mktime(self.m_firstTime)
        
    def toString(self):
        text = "%s, %d, %d, %s, %s, %d, %d, %.3f" % \
                    (self.m_strIMEI, \
                     self.m_nLac, \
                     self.m_nCellID, \
                     common_function.get_time_str(self.m_firstTime), \
                     common_function.get_time_str(self.m_endTime), \
                     self.m_dDuration, \
                     self.m_nRat, \
                     self.m_dMobility_speed)
        strApp = ""
        for x in self.m_lsApps:
            strApp += "%d; %d; %d; %d; %d; %d; %.3f; %.3f; %d; %d; %d" % \
                (x.m_nServiceType, \
                 x.m_nServiceGroup, \
                 x.m_nUpPackets, \
                 x.m_nDownPackets, \
                 x.m_nUpBytes, \
                 x.m_nDownBytes, \
                 x.m_dUpSpeed, \
                 x.m_dDownSpeed, \
                 x.m_nUserPort, \
                 x.m_nDstPort, \
                 x.m_nProtocol)
            strApp += ", "
        text = text + ", " + strApp
        return text
        
            