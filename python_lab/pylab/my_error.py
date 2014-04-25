# -*- coding: utf-8 -*-
'''
Created on 2014年4月25日

@author: y00752450
'''

class MyError(Exception):
    '''
        Exception in my code
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)