# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
from node import *
from tuple import *
from common_function import *




def extractPath(strImei, strInDir, lsInFiles, strOutDir):
    '''extract roaming path of given IMEI from CDR'''
    if len(lsInFiles) == 0 :
        raise NameError("Error: empty input file list")
    
    lsPath = list() # the roaming path
    strIMEI = strImei.strip()
    for strInFileName in lsInFiles:
        print("Begin to scan file: "+strInFileName+"\n")
        with open(strInDir+strInFileName) as hInFile:
            curNode = CNode("", 0, 0)
            
            while(1):
                lsLines = hInFile.readlines(MAX_PROC_MEM)
                if not lsLines:
                    break
                
                for line in lsLines:
                    try:
                        it = line.split(',')
                        if (len(it) != const_tuple_number or it[4].strip() != strIMEI): 
                            continue # unqualified line, skip it
                        
                        # parse line
                        tp = CTuple()
                        tp.parseFromStr(line)
                        
                        if (tp.m_strIMEI.strip() != strIMEI.strip() ): 
                            continue # not the given user, skip it!
                        
                        
                        
                        if (tp.m_nCellID != curNode.m_nCellID): #enter a new cell
                            newNode = CNode(tp.m_strIMEI, tp.m_nLac, tp.m_nCellID)
                            newNode.m_firstTime = tp.m_firstTime
                            newNode.m_endTime = tp.m_endTime
                            newNode.updateDuration()
                            newNode.m_nRat = tp.m_nRat
                            newNode.m_lsApps.append(tp.m_app)
                            if (curNode.m_nCellID != 0):
                                newNode.m_dMobility_speed = calcMobility(curNode, newNode)
                                
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
                            
                            lsPath[len(lsPath)-1] = curNode
                        
                    except NameError as err:
                        print(err)
                    except IndexError:
                        print "Index error, line=", line
                        raise
                        

    # Note: all the nodes of given IMEI will first store in MEM and then write to file
    print("Begin to serialize path to file...")
    strFilePath = serializePath(strIMEI, strOutDir, lsPath)
    tx = "extract path for IMEI:%s finished, #nodes=%d." % (strIMEI, len(lsPath) ) 
    print(tx)
    return lsPath

 
if __name__ == '__main__':
    lsImeis = ["0127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/export-userservice-2013100308.dat", \
             "/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/export-userservice-2013100309.dat"]
    strOutDir = "/mnt/disk12/yanglin/workspace/paths/"
    lsResult = extractPath("0127460079774812", lsCDR, strOutDir)

    