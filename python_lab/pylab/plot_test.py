# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 16:01:48 2014

@author: jason
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


sr = pd.Series(np.arange(10,15), index=['a1', 'a2', 'a3', 'a4', 'a5'])
df = pd.DataFrame({'c1':sr, 'c2':sr*2, 'c3':sr-5})

# create subplots
fig, axes = plt.subplots(nrows=1, ncols=2)

# plot
sr.plot(ax=axes[0], style='-o')
df.plot(ax=axes[1], kind='bar')

# set style
axes[0].set_ylabel('User Number')
axes[0].set_xlabel('App Categories')
axes[1].set_ylabel('User Number per Cell')
axes[1].set_xlabel('App Categories')


    