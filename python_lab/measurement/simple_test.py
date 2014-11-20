# -*- coding: utf-8 -*-
'''
Created on 2014年1月14日

@author: jason
'''
from common_function import *

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

 
def constructCellLocFromAdditionalSource(strPath):
    dcNew = {}
    with open(strPath) as hNew:
        for line in hNew:
            lsItems = line.split(',')
            if(len(lsItems) != 8 or False == lsItems[0].isdigit() ):
                continue
            strKey = "%s-%s" % (lsItems[0].strip(), lsItems[1].strip())
            loc = (0., 0.)
            try:
                if( lsItems[2] != '' and lsItems[3] != '' ):
                    loc=(float(lsItems[2]), float(lsItems[3]) )
            except ValueError as v:
                print("==>%s, %s" % (lsItems[2], lsItems[3]))
            dcNew[strKey] = loc

    return dcNew


def test(df):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    df['c1'].plot(ax=axes[0], label='c1')
    df['c2'].plot(ax=axes[0], label='c2')
    df['c3'].plot(ax=axes[1], label='c3')
    plt.legend()
    plt.show()



  
def findDiff(dfPrevious, dcNew):
    lsDis = []
    for tp in dfPrevious.itertuples():
        key = tp[0]
        dLat = float(tp[1])
        dLong = float(tp[2])
        
        newLoc = dcNew.get(key, (0., 0.) )
        
        if(newLoc != (0., 0.) and dLat != 0. and dLong != 0.):
            dis = calculateDistance(dLat, dLong, newLoc[0], newLoc[1])
            lsDis.append(dis)
        
    sDis = pd.Series(lsDis)
    sDis.describe()
    return sDis

def ensurePathExist(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


import matplotlib.pyplot as plt
import matplotlib.pyplot

def axes_broken_y(axes, upper_frac=0.5, break_frac=0.02, ybounds=None, 
                  xlabel=None, ylabel=None): 
    """ 
    Replace the current axes with a set of upper and lower axes. 

    The new axes will be transparent, with a breakmark drawn between them.  They 
    share the x-axis.  Returns (upper_axes, lower_axes). 

    If ybounds=[ymin_lower, ymax_lower, ymin_upper, ymax_upper] is defined, 
    upper_frac will be ignored, and the y-axis bounds will be fixed with the 
    specified values. 
    """ 
    def breakmarks(axes, y_min, y_max, xwidth=0.008): 
        x1, y1, x2, y2 = axes.get_position().get_points().flatten().tolist() 
        segment_height = (y_max - y_min) / 3. 
        xoffsets = [0, +xwidth, -xwidth, 0] 
        yvalues  = [y_min + (i * segment_height) for i in range(4)] 
        # Get color of y-axis 
        for loc, spine in axes.spines.iteritems(): 
            if loc  == 'left': 
                color = spine.get_edgecolor() 
        for x_position in [x1, x2]: 
            line = matplotlib.lines.Line2D( 
                [x_position + offset for offset in xoffsets], yvalues, 
                transform=plt.gcf().transFigure, clip_on=False, 
                color=color) 
            axes.add_line(line) 
    # Readjust upper_frac if ybounds are defined 
    if ybounds: 
        if len(ybounds) != 4: 
            print "len(ybounds) != 4; aborting..." 
            return 
        ymin1, ymax1, ymin2, ymax2 = [float(value) for value in ybounds] 
        data_height1, data_height2 = (ymax1 - ymin1), (ymax2 - ymin2) 
        upper_frac = data_height2 / (data_height1 + data_height2) 
    x1, y1, x2, y2 = axes.get_position().get_points().flatten().tolist() 
    width = x2 - x1 
    lower_height = (y2 - y1) * ((1 - upper_frac) - 0.5 * break_frac) 
    upper_height = (y2 - y1) * (upper_frac - 0.5 * break_frac) 
    upper_bottom = (y2 - y1) - upper_height + y1 
    lower_axes = plt.axes([x1, y1, width, lower_height], axisbg='None') 
    upper_axes = plt.axes([x1, upper_bottom, width, upper_height], 
                          axisbg='None', sharex=lower_axes) 
    # Erase the edges between the axes 
    for loc, spine in upper_axes.spines.iteritems(): 
        if loc == 'bottom': 
            spine.set_color('none') 
    for loc, spine in lower_axes.spines.iteritems(): 
        if loc == 'top': 
            spine.set_color('none') 
    upper_axes.get_xaxis().set_ticks_position('top') 
    lower_axes.get_xaxis().set_ticks_position('bottom') 
    plt.setp(upper_axes.get_xticklabels(), visible=False) 
    breakmarks(upper_axes, y1 + lower_height, upper_bottom) 
    # Set ylims if ybounds are defined 
    if ybounds: 
        lower_axes.set_ylim(ymin1, ymax1) 
        upper_axes.set_ylim(ymin2, ymax2) 
        lower_axes.set_autoscaley_on(False) 
        upper_axes.set_autoscaley_on(False) 
        upper_axes.yaxis.get_label().set_position((0, 1 - (0.5 / (upper_frac/(1+break_frac))))) 
        lower_axes.yaxis.get_label().set_position((0, 0.5 / ((1 - upper_frac)/(1+break_frac)))) 
    # Make original axes invisible 
    axes.set_xticks([]) 
    axes.set_yticks([]) 
#     print upper_axes.yaxis.get_label().get_position() 
#     print lower_axes.yaxis.get_label().get_position() 
#     print axes.yaxis.get_label().get_position() 
#     print axes.yaxis.labelpad 
    for loc, spine in axes.spines.iteritems(): 
        spine.set_color('none') 
    return upper_axes, lower_axes 

def prepare_efficiency(axes, lower_bound=0.69): 
    """ 
    Set up an efficiency figure with breakmarks to indicate a suppressed zero. 

    The y-axis limits are set to (lower_bound, 1.0), as appropriate for an 
    efficiency plot, and autoscaling is turned off. 
    """ 
    upper_axes, lower_axes = axes_broken_y(axes, upper_frac=0.97) 
    lower_axes.set_yticks([]) 
    upper_axes.set_ylim(lower_bound, 1.) 
    upper_axes.set_autoscaley_on(False) 
    return upper_axes, lower_axes 

# test these 
ax = plt.axes() 
upper, lower = axes_broken_y(ax, ybounds=[-2., 2.9, 22.1, 30.]) 
upper.plot(range(30), range(30)) 
lower.plot(range(30), range(30)) 
upper.set_ylabel('Data') 
plt.show()


if __name__ == '__main__':
    pass
