# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
from node import *
from tuple import *
from common_function import *
from path import *

import multiprocessing

MIN_NODE_DURATION = 10
MIN_NODE_UP_BYTES = 100
MIN_NODE_DOWN_BYTES = 100


# NOTE: this function will create an empty list for each given IMEI, this means if
#       there is no path was extracted for this imei, it will still return an CPath
#       instance with an empty list for this IMEI
def constructUserDict(lsImeis):
    dict = {}
    for strImei in lsImeis:
        path = CPath(strImei)
        dict[strImei] = path
    return dict

def refinePath(path):
    '''
        this function will:
        1. sort the path by first_time,
        2. merge the adjacent cells which have same lac and cell_id
        3. calculate the moving speed btw nodes if there is location info
    '''
    lsRefinedNodes = []
    path.m_lsNodes.sort(key=lambda node:node.m_firstTime)
    
    startIndex = 0
    endIndex = 0
    while(startIndex < len(path.m_lsNodes) ):
        while(endIndex < len(path.m_lsNodes) ):
            if(path.m_lsNodes[startIndex].m_nLac == path.m_lsNodes[endIndex].m_nLac and \
               path.m_lsNodes[startIndex].m_nCellID == path.m_lsNodes[endIndex].m_nCellID):
                endIndex += 1
            else:
                break
        merNode = mergeNodes(path.m_lsNodes[startIndex:endIndex])
        lsRefinedNodes.append(merNode)
        startIndex = endIndex
        
    # re-calculate moving speed btw nodes    
    i = 1
    while(i < len(lsRefinedNodes) ):
        lsRefinedNodes[i].m_dSpeed = calculateMobilitySpeed(lsRefinedNodes[i-1], lsRefinedNodes[i])
    if(len(lsRefinedNodes) >= 2):
        lsRefinedNodes[0].m_dSpeed = lsRefinedNodes[1].m_dSpeed

    path.m_lsNodes = lsRefinedNodes


def extractPath(dcCellLoc, lsImeis, strInDir, lsInFiles, strOutDir):
    '''
        extract roaming path of given IMEIs from CDR
    '''
    if len(lsInFiles) == 0 :
        raise StandardError("Error: empty input file list")
      
    dcPaths = constructUserDict(lsImeis)
    for strInFileName in lsInFiles:
        print("Proc: %s starts to scan file: %s" \
              % (multiprocessing.current_process().name, strInFileName) )
        
        with open(strInDir+strInFileName) as hInFile:
            while(1):
                lsLines = hInFile.readlines(MAX_IO_BUF_SIZE)
                if not lsLines: # break if there is no more lines
                    break
                
                for line in lsLines:
                    try:
                        it = line.split(',')
                        if (len(it) != ELEMENT_NUM_EACH_LINE): # unqualified line(invalid formated), skip it !
                            continue 
                        path = dcPaths.get(it[4].strip())
                        if(None == path):
                            continue
                        
                        # parse line
                        tuple = CTuple()
                        tuple.parseFromStr(line)
                        
                        if ( len(path.m_lsNodes) != 0 and tuple.m_nCellID != path.m_lsNodes[-1].m_nCellID ):# delete last node if its duration is too short
                            if (path.m_lsNodes[-1].m_dDuration < MIN_NODE_DURATION ):  
                                path.m_lsNodes.pop()
                        
                        if (len(path.m_lsNodes) == 0 or tuple.m_nCellID != path.m_lsNodes[-1].m_nCellID ): # enter a  new cell
                            newNode = CNode(tuple.m_strIMEI, tuple.m_nLac, tuple.m_nCellID)
                            newNode.m_dLat = dcCellLoc.get("%d-%d"%(tuple.m_nLac, tuple.m_nCellID), (0.0, 0.0))[0]
                            newNode.m_dLong = dcCellLoc.get("%d-%d"%(tuple.m_nLac, tuple.m_nCellID), (0.0, 0.0))[1]
                            newNode.m_firstTime = tuple.m_firstTime
                            newNode.m_endTime = tuple.m_endTime
                            newNode.updateDuration()
                            newNode.m_nRat = tuple.m_nRat
                            newNode.m_lsApps.append(tuple.m_app)
                            path.m_lsNodes.append(newNode)
                            
                        else: # still in current cell
                            path.m_lsNodes[-1].m_firstTime = min(path.m_lsNodes[-1].m_firstTime, tuple.m_firstTime)
                            path.m_lsNodes[-1].m_endTime = max(path.m_lsNodes[-1].m_firstTime, tuple.m_endTime)
                            path.m_lsNodes[-1].updateDuration()
                            path.m_lsNodes[-1].updateAppList(tuple.m_app)

                    except StandardError as err:
                        print(err)
    
       
    # refine the path
    for tuple in dcPaths.items():
        refinePath(tuple[1])
        tuple[1].updatePathInfo() # update path info
    
    return dcPaths

 
if __name__ == '__main__':
    lsImeis = ["8677470189216800", "0128480018959912", "8613440243171178"]
    lsCDR = ["new2.dat", \
            ]
    strInDir = "D:\\yanglin\\playground\\cdr\\"
    strOutDir = "D:\\yanglin\\playground\\out\\"
    dcCellLoc = constructCellLocDict("D:\\yanglin\\playground\\dict.csv")
    rt = extractPath(dcCellLoc, lsImeis, strInDir, lsCDR, strOutDir)
    print("dd")

    