# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
import cPickle
import sys

from app import *

def main():
    print "Hello~"
    foo(5)

def foo(n):
    print "I'm foo, with %d" % (n)
    
def serialize2File(strFileName, strOutDir, obj):
    if len(obj) != 0:
        strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(obj), strFileName)
        with open(strOutFilePath, 'w') as hOutFile:
            cPickle.dump(obj, hOutFile, protocol=0)
        return strOutFilePath
    else:
        raise NameError("Error: Empty roaming path")
    
def shareReadTest(nMode):
    if(nMode == "0"):
        with open("/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/export-userservice-2013100303.dat") as hFile:
            print("reading aggressively...")
            hFile.readlines(1024*1024*1024*5)
            print("===aggressive reading is done.")
    else:
        with open("/mnt/disk12/yanglin/mnt/d1/USERSERVICE/20131003/export-userservice-2013100303.dat") as hFile:
            print("reading line by line...")
            while(1):
                line = hFile.readline()
                if not line:
                    break
                print("line:"+line+"\n")
            print("===reading line by line is done")




if __name__ == '__main__':
    dict={}
    for x in range(10):
        strKey = "k%d" % (x)
        curApp = CApp(x,x)
        ls = range(x)
        dict[strKey] = (curApp, ls)

    rt = dict.get("k5")
    print rt[0].m_nServiceType
    for y in rt[1]:
        print y
        
    dict["k5"] = range(100)
        
    rt = dict.get("k5")
    for y in rt[1]:
        print y
        
    