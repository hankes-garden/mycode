# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *


if __name__ == '__main__':
    print("hello")
    dfServiceDict = getServiceDict("d:\\yanglin\\local\\work\\playground\\service_dict.csv")
    dcLocalApp = {}
    with open("d:\\yanglin\\local\\work\\playground\\info.txt") as hFile:
        lsLines = hFile.readlines(MAX_IO_BUF_SIZE)
        for line in lsLines:
            nServiceType = int(line.split(',')[0].split(':')[1])
            nUserNum = int(line.split(',')[1].split('=')[1])
            strName = dfServiceDict.loc[nServiceType]['ServiceName']
            dcLocalApp[dcLocalApp] = (nUserNum, strName)
    for tp in dcLocalApp.items():
        print("%d,%d,%s" % tp[0], tp[1][0], tp[1][1])
        
        

        
    