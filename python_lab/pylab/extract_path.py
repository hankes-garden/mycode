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
    '''extract roaming path of given IMEI from CDR'''
    if len(lsInFiles) == 0 :
        raise NameError("Error: empty input file list")
    
    dict = constructDict(lsImeis)
    for strInFileName in lsInFiles:
        print("Begin to scan file: "+strInFileName+"\n")
        with open(strInDir+strInFileName) as hInFile:
            while(1):
                lsLines = hInFile.readlines(MAX_PROC_MEM)
                if not lsLines:
                    break
                
                for line in lsLines:
                    try:
                        it = line.split(',')
                        if (len(it) != const_tuple_number or it[4].strip() not in dict): 
                            continue # unqualified line, skip it
                        
                        # parse line
                        tp = CTuple()
                        tp.parseFromStr(line)
                        
                        ls = dict.get(tp.m_strIMEI)
                        
                        if ( (len(ls) == 0) or (tp.m_nCellID != ls[-1].m_nCellID) ): #enter a new cell
                            newNode = CNode(tp.m_strIMEI, tp.m_nLac, tp.m_nCellID)
                            newNode.m_firstTime = tp.m_firstTime
                            newNode.m_endTime = tp.m_endTime
                            newNode.updateDuration()
                            newNode.m_nRat = tp.m_nRat
                            newNode.m_lsApps.append(tp.m_app)
                            if (len(ls)!=0):
                                newNode.m_dMobility_speed = calcMobility(ls[-1], newNode)
                                
                            ls.append(newNode)
                            
                        else: # still in current cell
                            ls[-1].m_firstTime = min(ls[-1].m_firstTime, tp.m_firstTime)
                            ls[-1].m_endTime = max(ls[-1].m_firstTime, tp.m_endTime)
                            ls[-1].updateDuration()
                            
                            index = ls[-1].findAppIndex(tp.m_app)
                            if (index != -1):  # already exists in the app list
                                ls[-1].m_lsApps[index].m_nUpPackets += tp.m_app.m_nUpPackets
                                ls[-1].m_lsApps[index].m_nDownPackets += tp.m_app.m_nDownPackets
                                ls[-1].m_lsApps[index].m_nUpBytes += tp.m_app.m_nUpBytes
                                ls[-1].m_lsApps[index].m_dUpSpeed = max(ls[-1].m_lsApps[index].m_dUpSpeed, tp.m_app.m_dUpSpeed)
                                ls[-1].m_lsApps[index].m_dDowSpeed = \
                                max(ls[-1].m_lsApps[index].m_dDownSpeed, tp.m_app.m_dDownSpeed)
                            else: # new app
                                ls[-1].m_lsApps.append(tp.m_app)
                            
                    except NameError as err:
                        print(err)
                    except IndexError:
                        print "Index error, line=", line
                        raise
                        

#     # Note: all the nodes of given IMEI will first store in MEM and then write to file at once
#     print("Begin to serialize paths to file...")
#     for key in dict.keys():
#         strFilePath = serializePath(key, strOutDir, dict.get(key) )
#     print("Serialization is done")

    print("Path extraction for given IMEIs is done")
    
    return dict

 
if __name__ == '__main__':
    lsImeis = ["0127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["export-userservice-2013100310-sample.dat", \
            ]
    strInDir = "D:\\yanglin\\mbb_mobility_measurement\\gz_xdr\\sample_data\\"
    strOutDir = "D:\\yanglin\\playground\\"
    rt = extractPath(lsImeis, strInDir, lsCDR, strOutDir)
    
    result_list = list()
    for path in rt.values():
        result_list.append(path)
        
    import measurement
    text = measurement.statistic(result_list)
    print text

    