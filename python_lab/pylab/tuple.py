# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *
from app import *
import time

ELEMENT_NUM_EACH_LINE = 31

class CTuple(object):
    '''
    a CDR record
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.m_firstTime = time.localtime()
        self.m_endTime = time.localtime()
        self.m_strIMEI = ''
        self.m_nLac = 0
        self.m_nCellID = 0

        self.m_nRat = 0
        self.m_app = CApp(0, 0)

        
    def parseFromStr(self, strline):
        lsItems = strline.split(',')
        if len(lsItems) != ELEMENT_NUM_EACH_LINE:
            raise StandardError("Could NOT parse this line correctly.")
        
        try :
            self.m_firstTime = reformat_time_string(lsItems[0])
            self.m_endTime = reformat_time_string(lsItems[1])
            self.m_strIMEI = lsItems[4]
            self.m_nLac = int(lsItems[7])
            self.m_nCellID = int(lsItems[9])
    
            self.m_app.m_nRat = int(lsItems[15])
            self.m_app.m_nServiceType = int(lsItems[16])
            self.m_app.m_nServiceGroup = int(lsItems[17])
            self.m_app.m_nUpPackets = int(lsItems[18])
            self.m_app.m_nDownPackets = int(lsItems[19]) 
            self.m_app.m_nUpBytes = int(lsItems[20])
            self.m_app.m_nDownBytes = int(lsItems[21])
            self.m_app.m_dUpSpeed = float(lsItems[22])
            self.m_app.m_dDownSpeed = float(lsItems[23])
            self.m_app.m_nUserPort = int(lsItems[26])
            self.m_app.m_nDstPort = int(lsItems[29])
            self.m_app.m_nProtocol = int(lsItems[27])
        except ValueError as err:
            print(err)
        
    def toString(self):
        text = "%s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %.3f, %.3f, %d, %d, %d" % \
                                      (get_time_str(self.m_firstTime), \
                                      get_time_str(self.m_endTime), \
                                      self.m_strIMEI, \
                                      self.m_nLac, \
                                      self.m_nCellID, \
                                      self.m_app.m_nRat, \
                                      self.m_app.m_nServiceType, \
                                      self.m_app.m_nServiceGroup, \
                                      self.m_app.m_nUpPackets, \
                                      self.m_app.m_nDownPackets, \
                                      self.m_app.m_nUpBytes, \
                                      self.m_app.m_nDownBytes, \
                                      self.m_app.m_dUpSpeed, \
                                      self.m_app.m_dDownSpeed, \
                                      self.m_app.m_nUserPort, \
                                      self.m_app.m_nDstPort, \
                                      self.m_app.m_nProtocol)
        return text
                                      
        