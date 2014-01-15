# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
import common_function
from node import *
from tuple import *


# some constants
g_max_buffer_size = 0
g_max_buffer_size = 1024*1024*512

@common_function.exeTime
def extractPath(strIMEI, strInFilePath, strOutDir):
    '''extract roaming path of given IMEI from CDR'''
    
    lsPath = list()
    with open(strInFilePath) as hInFile:
        hInFile.readline() # skip header
        curNode = CNode("", 0, 0)
        
        while(1):
            lsLines = hInFile.readlines(g_max_buffer_size)
            if not lsLines:
                break
            
            for line in lsLines:
                try:
                    tp = CTuple()
                    tp.parseFromStr(line)
                    
                    if (tp.m_strIMEI.strip() != strIMEI.strip() ): # not the given user, skip it!
                        continue
                    
                    if (tp.m_nCellID != curNode.m_nCellID): #enter a new cell
                        newNode = CNode(tp.m_strIMEI, tp.m_nLac, tp.m_nCellID)
                        newNode.m_firstTime = tp.m_firstTime
                        newNode.m_endTime = tp.m_endTime
                        newNode.updateDuration()
                        newNode.m_nRat = tp.m_nRat
                        newNode.m_lsApps.append(tp.m_app)
                        if (curNode.m_nCellID != 0):
                            newNode.m_dMobility_speed = common_function.calcMobility(curNode, newNode)
                            
                        lsPath.append(newNode)
                        curNode = newNode
                        
                    else: # still in current cell
                        curNode.m_firstTime = min(curNode.m_firstTime, tp.m_firstTime)
                        curNode.m_endTime = max(curNode.m_firstTime, tp.m_endTime)
                        curNode.updateDuration()
                        
                        index = curNode.findAppIndex(tp.m_app)
                        if (index != -1):  # already exists in the app list
                            curNode.m_lsApps[index].m_nUpPackets += tp.m_app.m_nUpPackets
                            curNode.m_lsApps[index].m_nDownPackets += tp.m_app.m_nDownPackets
                            curNode.m_lsApps[index].m_nUpBytes += tp.m_app.m_nUpBytes
                            curNode.m_lsApps[index].m_dUpSpeed = max(curNode.m_lsApps[index].m_dUpSpeed, tp.m_app.m_dUpSpeed)
                            curNode.m_lsApps[index].m_dDowSpeed = \
                            max(curNode.m_lsApps[index].m_dDownSpeed, tp.m_app.m_dDownSpeed)
                        else: # new app
                            curNode.m_lsApps.append(tp.m_app)
                        
                        lsPath.pop()
                        lsPath.append(curNode)
                    
                except NameError as err:
                    print(err)

        # Note: all the nodes of given IMEI will first store in MEM and then write to file 
        if len(lsPath) != 0:            
            text = ""         
            for x in lsPath:
                text += x.toString()
                text += "\n"
            # get path info
            info = common_function.getPathInfo(lsPath)
            text += info.toString()
            strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(lsPath), strIMEI)
            with open(strOutFilePath, 'w') as hOutFile:
                hOutFile.write(text)
        else:
            raise NameError("Error: Empty roaming path")
                    
        
if __name__ == '__main__':
    extractPath("127460079774812", "D:\\test.csv", "d:\\")

    