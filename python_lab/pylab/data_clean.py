# -*- coding: utf-8 -*-

'''
Created on 2014年4月9日

@author: jason
'''
from common_function import *
import pandas as pd

def outputMissingLocation(strInPath, strOutPath):
    '''
        output the cells whose location info is missing in the given cell_loc_dict
        and format output in order to leverage third-party app to fill missing value
    '''
    with open(strInPath) as hInFile:
        with open(strOutPath, 'w') as hOutFile:
            for line in hInFile:
                lsItems = line.split(',')
                if (len(lsItems) < 5 or False == lsItems[0].isdigit() ):
                    continue
                nLac = int(lsItems[0])
                nCID = int(lsItems[1])
                
                if (lsItems[3] == '' or lsItems[4] == '' ):
                    hOutFile.write("%d,%d,20120403,07:37:02\n" % (nLac, nCID) )
    print("output missing cell is finished.")
                
def fillMissingLocation(strInPath, strAdditionalInfoPath, strOutPath):
    '''
        fill the missing location by using additional info
    '''
    # construct dcCellLoc from old format
    dcCellLoc = {}
    with open(strInPath) as hLocDict:
        while(1):
            hLocDict.readline() # skip head
            lsLines = hLocDict.readlines(MAX_IO_BUF_SIZE)
            if not lsLines:
                break
            
            for line in lsLines:
                items = line.split(',')
                key = items[2]
                if(key!=""):
                    value = (0., 0.)
                    if (items[3]!="" and items[4]!=""):
                        value = (float(items[3]), float(items[4]) )
                    dcCellLoc[key] = value
    
    # fill the missing location
    with open(strAdditionalInfoPath) as hFile:
        for line in hFile:
            lsItem = line.split(",")
            if(len(lsItem) < 4):
                continue
            strKey = "%s-%s" % (lsItem[0], lsItem[1])
            loc = (0., 0.)
            if(lsItem[2]!='null' and lsItem[3]!='null'):
                loc = (float(lsItem[2]), float(lsItem[3]))
                
            if( (0., 0.)==dcCellLoc.get(strKey, (0., 0.)) ):
                dcCellLoc[strKey] = loc
                
    # output filled dc
    with open(strOutPath, 'w') as hOutFile:
        for tp in dcCellLoc.items():
            strLine = "%s,%s,%s" % (tp[0], tp[1][0], tp[1][1])
            hOutFile.write(strLine)
            
    print("Filling missing location is finished.")


if __name__ == '__main__':
#     strMissingPath = "d:\\yanglin\\local\\work\\playground\\missing_location.csv"
#     outputMissingLocation("d:\\yanglin\\local\\work\\playground\\dict.csv", strMissingPath)
    fillMissingLocation("d:\\yanglin\\local\\work\\playground\\dict.csv", "d:\\yanglin\\local\\work\\playground\\celloutput.txt", \
                        "d:\\yanglin\\local\\work\\playground\\cell_loc.csv")
    
    
    