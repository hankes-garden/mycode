# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jason

'''

class CPathInfo(object):
    '''
    definition of mobility
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.m_strIMEI = ""
        self.m_nPathLen = 0;
        self.m_dMobility = 0.0
        # uplink
        self.m_nUpBytes = 0
        self.m_nUpPackets = 0
        self.m_dMaxUpSpeed = 0
        self.m_dMinUpSpeed = 1000000000000000000000.0
        self.m_dAvgUpSpeed = 0.0
        # downlink
        self.m_nDownBytes = 0
        self.m_nDownPackets = 0
        self.m_dMaxDownSpeed = 0
        self.m_dMinDownSpeed = 1000000000000000000000.0
        self.m_dAvgDownSpeed = 0.0
        
    def toString(self):
        text = "%s, %d, %.3f, %d, %d, %.3f, %.3f, %.3f, %d, %d, %.3f, %.3f, %.3f" % \
                    (self.m_strIMEI, \
                     self.m_nPathLen, \
                     self.m_dMobility, \
                     self.m_nUpBytes, \
                     self.m_nUpPackets, \
                     self.m_dMaxUpSpeed, \
                     self.m_dMinUpSpeed, \
                     self.m_dAvgUpSpeed, \
                     self.m_nDownBytes, \
                     self.m_nDownPackets, \
                     self.m_dMaxDownSpeed, \
                     self.m_dMinDownSpeed, \
                     self.m_dAvgDownSpeed)

        return text
        