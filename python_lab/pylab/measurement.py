# -*- coding: utf-8 -*-
'''
Created on 2014年1月16日

@author: jason
'''

from common_function import *
from extract_path import *

import multiprocessing

result_list = []

def log_result(rt):
    result_list.append(rt)
    
def proc_init():
    print("Starting proc:", multiprocessing.current_process().name )
    
def extractPathinParallel(lsImeis, lsCDRFilePaths, strOutDir):
    nPoolSize = min(len(lsImeis), multiprocessing.cpu_count()*2)
    pool = multiprocessing.Pool(processes=nPoolSize, initializer=proc_init)
    for strImei in lsImeis:
        pool.apply_async(extractPath, args=(strImei, lsCDRFilePaths, strOutDir), callback = log_result)
    pool.close()
    pool.join()
    print(result_list[0][0].m_strIMEI)
    
        
if __name__ == '__main__':
    lsImeis = ["127460079774812", "0128480018959912", "8613440243171178"]
    lsCDR = ["D:\\yanglin\\local\\work\\playground\\t1.csv", \
             "D:\\yanglin\\local\\work\\playground\\t2.csv", \
             "D:\\yanglin\\local\\work\\playground\\t3.csv"]
    strOutDir = "D:\\yanglin\\local\\work\\playground\\"
    extractPathinParallel(lsImeis, lsCDR, strOutDir)
