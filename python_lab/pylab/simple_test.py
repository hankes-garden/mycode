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
    strSerializedPath = \
    "D:\\yanglin\\playground\\serPath_719_new1_new2.txt"
    lsPaths = deserializeFromFile(strSerializedPath)
    findOutliers(lsPaths, 2)
    print("done")
#     traceUser(lsPaths, "3551670557119501")
    

        
    