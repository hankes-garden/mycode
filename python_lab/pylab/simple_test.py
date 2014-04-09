# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *
import pandas as pd

def outputMissingLocation(dfCellLocation, strOutPath):
    with open(strOutPath, 'w') as hOutFile:
        for it in dfCellLocation.itertuples():
            if pd.isnull(it[1]):
                strLac = it[0].split('-')[0].strip()
                strCID = it[0].split('-')[1].strip()
                hOutFile.write("%s,%s,20120403,07:37:02\n" % (strLac, strCID) )

      
if __name__ == '__main__':
    pass    
        
        

        
    
