# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *

def outputLocalAppLocation(dcLocalApp, strOutPath):
    with open(strOutPath, 'w') as hOutFile:
        hOutFile.write("serviceType, lac-cid, lat, long, attributes\n")
        for nServiceType in dcLocalApp.keys():
            lsTopCells = dcLocalApp.get(nServiceType)
            for tp in lsTopCells:
                strLine = "%d, %s,%.6f,%.6f, %d\n" % (nServiceType, tp[0], tp[1][0], tp[1][1], tp[2])
                hOutFile.write(strLine)
    print("finished")
        

if __name__ == '__main__':
    pass    
        
        

        
    