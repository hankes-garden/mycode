# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jason
'''

class CApp(object):
    '''
    Detail info about an application
    '''


    def __init__(self, nServiceType, nServiceGroup):
        '''
        Constructor
        '''
        self.m_nServiceType = nServiceType
        self.m_nServiceGroup = nServiceGroup
        self.m_nUpPackets = 0
        self.m_nDownPackets = 0 
        self.m_nUpBytes = 0
        self.m_nDownBytes = 0
        self.m_dUpSpeed = 0.0
        self.m_dDownSpeed = 0.0
        self.m_nUserPort = 0
        self.m_nDstPort = 0
        self.m_nProtocol = 0