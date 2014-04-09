# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *

def selectPOIByCity(strPOIPath, strOutPath, strCityCode):
    strCityCode = strCityCode.strip()
    with open(strPOIPath) as hInFile:
        with open(strOutPath, 'w') as hOutFile:
            for line in hInFile:
                lsItems = line.split(',')
                if (len(lsItems) != 9):
                    continue
                if(lsItems[3].strip('\"') == strCityCode):
                    strLine = "%s, %s, %s, %s, %s, %s, %s, %s\n" % \
                    (lsItems[1].strip('\"'), lsItems[2].strip('\"'), lsItems[3].strip('\"'),\
                      lsItems[4].strip('\"'), lsItems[5].strip('\"'), lsItems[6].strip('\"'), \
                      lsItems[7].strip('\"'), lsItems[8].strip('\" '))
                    hOutFile.write(strLine)
    print("selectPOIByCity is finished.")



if __name__ == '__main__':
    pass

