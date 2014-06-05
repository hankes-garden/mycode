# -*- coding: utf-8 -*-
'''
Created on 2014��6��5��

@author: lyangab
'''

import pandas as pd

def findHeavyUser(dcTotalPaths, nTop):
    '''
        find paths for heavy users
        
        return:
                dfUserTraffic - a dataframe like: {imei: {'up_bytes', 'down_bytes'}}
                dcHeavyUserPaths - a dict of paths for top users
                
    '''
    
    lsData = []
    for path in dcTotalPaths.values():
        nUpBytes = 0
        nDownBytes = 0
        for node in path.m_lsNodes:
            for app in node.m_lsApps:
                nUpBytes += app.m_nUpBytes
                nDownBytes += app.m_nDownBytes
        lsData.append({'imei': path.m_strIMEI, 'up_bytes': nUpBytes, 'down_bytes': nDownBytes})

    dfUserTraffic = pd.DataFrame(lsData)
    dfUserTraffic.set_index('imei', inplace=True)
    
    # find top users by traffic
    dfUserTraffic.sort(column = 'down_bytes', ascending=False, inplace=True)
    
    lsHeavyUsers = dfUserTraffic.iloc[:nTop].index
    dcHeavyUserPaths = {}
    for tp in dcTotalPaths.items():
        if tp[0] in lsHeavyUsers:
            dcHeavyUserPaths[tp[0]] = tp[1]
    
    
    return dfUserTraffic, dcHeavyUserPaths
    


if __name__ == '__main__':
    pass