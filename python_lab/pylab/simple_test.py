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
    "D:\\yanglin\\mbb_mobility_measurement\\gz_xdr\\mobility\\app_mobility\\serPath_71906_export-userservice-2013100318_export-userservice-2013100321.txt"
    lsPaths = deserializeFromFile(strSerializedPath)
#     findOutliers(lsPaths)
    traceUser(lsPaths, "3551670557119501")
    

        
    