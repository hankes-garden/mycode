# -*- coding: utf-8 -*-
'''
Created on 2014年4月25日

@author: jason
'''

g_lsWebBrowsing = range(1002, 1007)

g_lsP2P = range(2001, 2038)

g_lsIM = range(3001, 3030)

g_lsReading = range(4001, 4017)

g_lsSNS = range(5001, 5006)
g_lsSNS.append(range(21001, 21011) )

g_lsVideo = range(6001, 6057)
g_lsVideo.append(range(7001, 7005) )

g_lsMusic = range(8001, 8017)

g_lsAppMarket = range(9001, 9004)

g_lsGame = range(10001, 10116)

g_lsEmail = range(11001, 11018)

g_lsStock = range(16001, 16013)

g_lsShopping = range(22001, 22006)

g_lsMap = range(26001, 26004)

g_strWebBrowsing = "web_browsing"

g_strP2P = "p2p"

g_strIM = "instant_messager"

g_strReading = "reading"

g_strSNS = "social_networks"

g_strVideo = "video"

g_strMusic = "music"

g_strAppMarket = "app_market"

g_strGame = "game"

g_strEmail = "email"

g_strStock = "stock"

g_strShopping = "shopping"

g_strMap = "map"

g_dcCategory = {g_strWebBrowsing:g_lsWebBrowsing, \
                g_strP2P: g_lsP2P, \
                g_strIM: g_lsIM, \
                g_strReading: g_lsReading, \
                g_strSNS: g_lsSNS, \
                g_strVideo: g_lsVideo, \
                g_strMusic: g_lsMusic, \
                g_strAppMarket: g_lsAppMarket, \
                g_strGame: g_lsGame, \
                g_strEmail: g_lsEmail, \
                g_strStock: g_lsStock, \
                g_strShopping: g_lsShopping, \
                g_strMap: g_lsMap }