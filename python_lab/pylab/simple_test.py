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
    
def serializePath(strIMEI, strOutDir, lsPath):
    if len(lsPath) != 0:
        strOutFilePath = "%s%d_%s.txt" % (strOutDir, len(lsPath), strIMEI)
        with open(strOutFilePath, 'w') as hOutFile:
            cPickle.dump(lsPath, hOutFile, protocol=0)
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
    ls = list()
    for x in range(3):
        ap = CApp(x,x)
        ls.append(ap)
    ls[len(ls)-1] = CApp(9,9)
    print ls
    
    