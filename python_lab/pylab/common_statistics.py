# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def drawCDF(data, nXStart, nXStop, nXStep=1, strTitle="CDF"):
    '''
        Draw CDF for all the columns in the data
    '''
    
    fig = plt.figure()
    spCDF = fig.add_subplot(111)
    spCDF.set_color_cycle(['r','g','b','c','y','m','k'])
    spCDF.set_xticks(range(nXStart,nXStop, nXStep))
    spCDF.set_xlim((nXStart, nXStop))
    spCDF.set_ylim(0.0, 1.0)
    spCDF.set_title(strTitle)
        
    for col in data.columns:
        cdf = data[col].order(ascending=False).cumsum()/data[col].sum()
        spCDF.plot(cdf,'-',label=col)

    spCDF.legend(loc='best')
    fig.show()


def drawUserCDF(data):
    #user cdf of user mobility
    http_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[1].cumsum()
    im_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[3].cumsum()
    weibo_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[5].cumsum()
    video_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[6].cumsum()
    video_cumsum.add(data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[7].cumsum(), fill_value=0)
    game_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[10].cumsum()
    email_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[11].cumsum()
    shopping_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[22].cumsum()
    map_cumsum = data.groupby(['ServiceGroup', 'Mobility'])['UserNum'].sum()[26].cumsum()
    
    
    http_cdf = http_cumsum/http_cumsum.iloc[-1]
    im_cdf = im_cumsum/im_cumsum.iloc[-1]
    weibo_cdf = weibo_cumsum/weibo_cumsum.iloc[-1]
    video_cdf = video_cumsum/video_cumsum.iloc[-1]
    game_cdf = game_cumsum/game_cumsum.iloc[-1]
    email_cdf = email_cumsum/email_cumsum.iloc[-1]
    shopping_cdf = shopping_cumsum/shopping_cumsum.iloc[-1]
    map_cdf = map_cumsum/map_cumsum.iloc[-1]
    
    fig = plt.figure()
    fig_user_cdf = fig.add_subplot(111)
    fig_user_cdf.plot(http_cdf, 'b-', label='http')
    fig_user_cdf.plot(im_cdf, 'g-', label='im')
    fig_user_cdf.plot(weibo_cdf, '-',color='0.71', label='weibo')
    fig_user_cdf.plot(video_cdf, 'c-', label='video')
    fig_user_cdf.plot(game_cdf, 'm-', label='game')
    fig_user_cdf.plot(email_cdf, 'y-', label='email')
    fig_user_cdf.plot(shopping_cdf, 'k-', label='shopping')
    fig_user_cdf.plot(map_cdf, 'r-',label='map')
    fig_user_cdf.set_xticks(range(10))
    fig_user_cdf.set_xlim(0, 10)
    fig_user_cdf.set_ylim(0.7, 1.0)
    fig_user_cdf.set_xlabel('Moving speed level')
    fig_user_cdf.set_title('Appilcation User Number CDF of User Moving Speed')
    fig_user_cdf.legend(loc='best')
    fig.show()


def plotSubGroups(grouped, strColumnName, aggFunction, nXLim, nYLim):
    #application mobility dynamics on user mobility
    aggregatedSubgroup = grouped[strColumnName].agg(aggFunction)
    fig = plt.figure()
    fig_sub_group = fig.add_subplot(111)
    fig_sub_group.set_color_cycle(['r','g','b','c','y','m','k'])
    for i in [1,3,5,6,7,10,11,22,26]:
        fig_sub_group.plot(aggregatedSubgroup.loc[i],'-')
    fig_sub_group.set_xlim(0, nXLim)
    fig_sub_group.set_ylim(0, nYLim)
    fig.show()
    
# if __name__ == '__main__':
#     # load data
#     col_name = ['Mobility','ServiceType', 'ServiceGroup', 'UserNum', 'AvgCellNum', 'TotalUpBytes', 
#             'AvgUpBytes', 'MaxUpBytes', 'MinUpBytes', 'AvgUpSpeed', 'MaxUpSpeed', 
#             'MinUpSpeed', 'TotalDownBytes', 'AvgDownBytes', 'MaxDownBytes', 
#             'MinDownBytes', 'AvgDownSpeed', 'MaxDownSpeed', 'MinDownSpeed', 
#             'Protocol', 'UserPort', 'DstPort']
#     
#     cell_data = pd.read_csv("../results/appMob_719066_2013100318_2013100321_speed.txt", 
#     header=None, names=col_name)
# 
#     # drawUserCDF(cell_data)
#     
#     ## group data
#     #grouped = cell_data.groupby(['ServiceGroup', 'Mobility']) 
#     #
    #plotSubGroups(grouped, 'AvgCellNum', np.average, 30, 30)
    #
    


