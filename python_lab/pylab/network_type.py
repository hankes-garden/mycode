# -*- coding: utf-8 -*-
'''
Created on 2014��6��5��

@author: lyangab
'''
ID_NETWORK_3G = 1 
ID_NETWORK_2G = 2


def getNetworks(dcTotalPaths):
    '''
        get paths of 2G and 3G
    '''
    dc2G = {}
    dc3G = {}
    
    b3G = False
    for tp in dcTotalPaths.items():
        key = tp[0]
        path = tp[1]
        for node in path.m_lsNodes:
            if (node.m_nRat == ID_NETWORK_3G) : # if this user ever uses 3G in one node, then he/she is 3G user
                b3G = True
                break
        
        if (b3G):
            dc3G[key] = path
        else:
            dc2G[key] = path
            
    return dc2G, dc3G
    

if __name__ == '__main__':
    pass