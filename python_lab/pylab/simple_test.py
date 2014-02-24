# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
import cPickle
import sys

from app import *
from common_function import *
from extract_path import *


if __name__ == '__main__':
    print("start!")
    lsPaths = deserializeFromFile("D:\yanglin\playground\serPath_71906_export-userservice-2013100311_export-userservice-2013100315.txt")
    for path in lsPaths:
        if path[0].m_strIMEI == "3551670557119501":
            for node in path:
                print("node: lac=%d, cellID=%d, duration=%.2f, %s, %s" % \
                      (node.m_nLac, node.m_nCellID, node.m_dDuration,\
                       get_time_str(node.m_firstTime), get_time_str(node.m_endTime)))
                
    print("end!")
    

        
    