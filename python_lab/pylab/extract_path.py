# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
from node import *
from tuple import *
from common_function import *

MIN_NODE_DURATION = 10
MIN_NODE_UP_BYTES = 100
MIN_NODE_DOWN_BYTES = 100


# NOTE: this function will create an empty list for each given IMEI, this means if
#       there is no path was extracted for this imei, it will still return an empty
#       list for this IMEI
def constructDict(lsImeis):
    dict = {}
    for strImei in lsImeis:
        lsPath = list()
        dict[strImei.strip()] = lsPath
    return dict

def refinePath(lsPath):
    '''
        this function will:
        1. sort the path by first_time,
        2. merge the adjacent cells which have same lac and cell_id
    '''
    lsRefinedPath = []
    lsPath.sort(key=lambda node:node.m_firstTime)
    
    startIndex = 0
    endIndex = 0
    while(startIndex < len(lsPath) ):
        while(endIndex < len(lsPath) ):
            if(lsPath[startIndex].m_nLac == lsPath[endIndex].m_nLac and \
               lsPath[startIndex].m_nCellID == lsPath[endIndex].m_nCellID):
                endIndex += 1
            else:
                break
        merNode = mergeNodes(lsPath[startIndex:endIndex])
        lsRefinedPath.append(merNode)
        startIndex = endIndex
        
    return lsRefinedPath

def extractPath(lsImeis, strInDir, lsInFiles, strOutDir):
    '''
        extract roaming path of given IMEI from CDR
    '''
    if len(lsInFiles) == 0 :
        raise StandardError("Error: empty input file list")
    
    dcPaths = constructDict(lsImeis)
    for strInFileName in lsInFiles:
        print("Begin to scan file: "+strInFileName)
        
        with open(strInDir+strInFileName) as hInFile:
            while(1):
                lsLines = hInFile.readlines(MAX_IO_BUF_SIZE)
                if not lsLines: # break if there is no more lines
                    break
                
                for line in lsLines:
                    try:
                        it = line.split(',')
                        if (len(it) != ELEMENT_NUM_EACH_LINE or it[4].strip() not in dcPaths): 
                            continue # unqualified line(invalid formated or not we want), skip it !
                        
                        # parse line
                        tp = CTuple()
                        tp.parseFromStr(line)
                        
                        lsPath = dcPaths.get(tp.m_strIMEI)
                        
                        if ( len(lsPath) != 0 and tp.m_nCellID != lsPath[-1].m_nCellID ): # enter a  new cell
                            if (lsPath[-1].m_dDuration < MIN_NODE_DURATION ): # delete last node if its duration is short 
                                lsPath.pop()
                        
                        if (len(lsPath) == 0 or tp.m_nCellID != lsPath[-1].m_nCellID ):
                            newNode = CNode(tp.m_strIMEI, tp.m_nLac, tp.m_nCellID)
                            newNode.m_firstTime = tp.m_firstTime
                            newNode.m_endTime = tp.m_endTime
                            newNode.updateDuration()
                            newNode.m_nRat = tp.m_nRat
                            newNode.m_lsApps.append(tp.m_app)
                            if (len(lsPath)!=0):
                                newNode.m_dMobility_speed = calcMobility(lsPath[-1], newNode)
                            
                            lsPath.append(newNode)
                            
                        else: # still in current cell
                            lsPath[-1].m_firstTime = min(lsPath[-1].m_firstTime, tp.m_firstTime)
                            lsPath[-1].m_endTime = max(lsPath[-1].m_firstTime, tp.m_endTime)
                            lsPath[-1].updateDuration()
                            lsPath[-1].updateAppList(tp.m_app)

                    except StandardError as err:
                        print(err)

    # refine the path
    dcRefinedPaths = {}
    for tp in dcPaths.items():
        dcRefinedPaths[tp[0]] = refinePath(tp[1])
    
    return dcRefinedPaths

 
if __name__ == '__main__':
    lsImeis = ["0127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["new2.dat", \
            ]
    strInDir = "D:\\yanglin\\playground\\cdr\\"
    strOutDir = "D:\\yanglin\\playground\\out\\"
    rt = extractPath(lsImeis, strInDir, lsCDR, strOutDir)
    print("dd")

    