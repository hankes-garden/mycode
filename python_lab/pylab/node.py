# -*- coding: utf-8 -*-
'''
Created on 2014年1月15日

@author: jason
'''
from common_function import *
import time
import copy

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
        self.m_dLat = 0.0
        self.m_dLong = 0.0
        
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
    
    def updateAppList(self, app):
        index = self.findAppIndex(app)
        if (index != -1):  # already exists in the app list
            self.m_lsApps[index].m_nUpPackets += app.m_nUpPackets
            self.m_lsApps[index].m_nDownPackets += app.m_nDownPackets
            self.m_lsApps[index].m_nUpBytes += app.m_nUpBytes
            self.m_lsApps[index].m_nDownBytes += app.m_nDownBytes
            self.m_lsApps[index].m_dUpSpeed = max(self.m_lsApps[index].m_dUpSpeed, app.m_dUpSpeed)
            self.m_lsApps[index].m_dDowSpeed = \
            max(self.m_lsApps[index].m_dDownSpeed, app.m_dDownSpeed)
        else: # new app
            self.m_lsApps.append(copy.deepcopy(app))
    
    def updateDuration(self):
        self.m_dDuration = time.mktime(self.m_endTime) - time.mktime(self.m_firstTime)
        
    def toString(self):
        text = "%s, %d, %d, %.6f, %.6f, %s, %s, %d, %d, %.3f" % \
                    (self.m_strIMEI, \
                     self.m_nLac, \
                     self.m_nCellID, \
                     self.m_dLat, \
                     self.m_dLong, \
                     get_time_str(self.m_firstTime), \
                     get_time_str(self.m_endTime), \
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
        
        
def mergeNodes(lsNodes):
    '''
        this function merge a list of nodes to a single node
    '''
    if len(lsNodes) == 0:
        raise StandardError("Error: try to merge empty node list.")
    
    if len(lsNodes) == 1:
        return lsNodes[0]
    
    mergedNode = CNode(lsNodes[0].m_strIMEI, lsNodes[0].m_nLac, lsNodes[0].m_nCellID)
    mergedNode.m_dLat = lsNodes[0].m_dLat
    mergedNode.m_dLong = lsNodes[0].m_dLong
    mergedNode.m_firstTime = min(lsNodes, key=lambda node: node.m_firstTime).m_firstTime
    mergedNode.m_endTime = max(lsNodes, key=lambda node: node.m_endTime).m_endTime
    mergedNode.updateDuration()
    
    for node in lsNodes:
        for app in node.m_lsApps:
            mergedNode.updateAppList(app)
    
    # TODO: this might be a bug: 
    #       1. if user switches btw 2G/3G in a single cell
    #       2. mobile speed of merged node 
    mergedNode.m_nRat = lsNodes[0].m_nRat
    mergedNode.m_dMobility_speed = max(lsNodes, key=lambda node:node.m_dMobility_speed).m_dMobility_speed
    
    return mergedNode