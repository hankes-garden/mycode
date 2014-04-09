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
                if(lsItems[3].strip == strCityCode):
                    strLine = "%s, %s, %s, %s, %s, %s, %s, %s\n" % (lsItems[1], lsItems[2], lsItems[3], lsItems[4], lsItems[5], lsItems[6], lsItems[7], lsItems[8])
                    hOutFile.write(strLine)
    print("selectPOIByCity is finished.")
                

      
if __name__ == '__main__':
    pass    
        
        

        
    
