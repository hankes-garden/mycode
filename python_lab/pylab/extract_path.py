# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''

from app import *
from node import *
from tuple import *
from common_function import *

# NOTE: this function will create an empty list for each given IMEI, this means if
#       there is no path was extracted for this imei, it will still return an empty
#       list for this IMEI
def constructDict(lsImeis):
    dict = {}
    for strImei in lsImeis:
        lsPath = list()
        dict[strImei.strip()] = lsPath
    return dict
    


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
                        
                        if ( (len(lsPath) == 0) or (tp.m_nCellID != lsPath[-1].m_nCellID) ): #enter a new cell
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
                            
                            index = lsPath[-1].findAppIndex(tp.m_app)
                            if (index != -1):  # already exists in the app list
                                lsPath[-1].m_lsApps[index].m_nUpPackets += tp.m_app.m_nUpPackets
                                lsPath[-1].m_lsApps[index].m_nDownPackets += tp.m_app.m_nDownPackets
                                lsPath[-1].m_lsApps[index].m_nUpBytes += tp.m_app.m_nUpBytes
                                lsPath[-1].m_lsApps[index].m_dUpSpeed = max(lsPath[-1].m_lsApps[index].m_dUpSpeed, tp.m_app.m_dUpSpeed)
                                lsPath[-1].m_lsApps[index].m_dDowSpeed = \
                                max(lsPath[-1].m_lsApps[index].m_dDownSpeed, tp.m_app.m_dDownSpeed)
                            else: # new app
                                lsPath[-1].m_lsApps.append(tp.m_app)
                            
                    except StandardError as err:
                        print(err)

    return dcPaths

 
if __name__ == '__main__':
    lsImeis = ["0127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["export-userservice-2013100310-sample.dat", \
            ]
    strInDir = "D:\\yanglin\\mbb_mobility_measurement\\gz_xdr\\sample_data\\"
    strOutDir = "D:\\yanglin\\playground\\"
    rt = extractPath(lsImeis, strInDir, lsCDR, strOutDir)
    
    g_lsPaths = list()
    for path in rt.values():
        g_lsPaths.append(path)
        
    import measurement
    text = measurement.statistic(g_lsPaths)
    print text

    