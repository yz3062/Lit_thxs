#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 22:18:16 2022

@author: zhou
"""

import matplotlib.pyplot as plt
import seaborn as sns
# import matplotlib.lines as mlines
# import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
# import xarray
from matplotlib.lines import Line2D

sns.set(font='Arial',palette='husl',style='ticks', context='paper')#, context='talk', font_scale=0.8)

# In Sv
ylim_lower = 3e-3
ylim_upper = 3e-1

labels=np.array(['YD', 'H1', 'H2', 'H3',
                 'H4', 'H5', 'H6', 'HQ',
                 'H1/2', 'H1/2/\n4/5'])

freshwater = np.array([0.0035881587639718577, 0.015579380965302864, 0.027807440666916795, 0.0033215418882363,
                       0.12988038473319954, 0.026201032214862863, 0.010467184843468993, 0.013728162797842426,
                       0.016, 0.04])
# freshwater = freshwater * 1000

freshwater_relative_std_lower = np.array([0.7256525625336429, 0.6099604478174043, 0.5262724404033389, 0.696263936926466,
                                          0.7900211193660226, 0.8778272530963053, 1.0711518345010922, 1.2943561685959266,
                                    0, 0.5])
freshwater_relative_std_upper = np.array([0.7256525625336429, 0.6099604478174043, 0.5262724404033389, 0.696263936926466,
                                          0.7900211193660226, 0.8778272530963053, 1.0711518345010922, 1.2943561685959266,
                                    0, 1])# For Roberts, RSD is 1 cuz SD is 1:1 as the value itself
freshwater_std_lower = np.multiply(freshwater, freshwater_relative_std_lower)
freshwater_std_upper = np.multiply(freshwater, freshwater_relative_std_upper)
# freshwater_std = freshwater_std

freshwater_sorted = np.take(freshwater, np.argsort(freshwater))
labels_sorted = np.take(labels, np.argsort(freshwater))
freshwater_std_sorted_lower = np.take(freshwater_std_lower, np.argsort(freshwater))
freshwater_std_sorted_upper = np.take(freshwater_std_upper, np.argsort(freshwater))

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

# Enderlin2014_df = pd.read_excel('Enderlin2014.xlsx')
# Bamber2018_xr = xarray.open_dataset('Bamber2018/FWF17.v3_b.nc')
# D = Bamber2018_xr['solid_ice'].sum(dim=['X', 'Y'])
# convert from monthly to annually
# Source: https://ncar.github.io/esds/posts/2021/yearly-averages-xarray/
# D = D.resample(TIME='AS').mean('TIME')
D = [31.77442 , 34.636253, 36.147167, 35.352837, 35.284668, 34.99967 ,
        33.05917 , 31.868834, 32.59992 , 31.940834, 32.671505, 33.672085,
        33.30517 , 33.04342 , 32.027584, 30.705833, 30.519836, 31.403666,
        30.488585, 31.574919, 32.07758 , 31.634169, 31.7555  , 32.693836,
        32.861835, 32.12542 , 32.687004, 32.902416, 31.770418, 32.333668,
        33.72617 , 34.016087, 34.282837, 35.180504, 32.302082, 32.351917,
        32.402836, 32.453754, 32.486668, 32.839672, 33.210835, 34.398754,
        37.179836, 37.575085, 38.72492 , 39.915165, 40.7885  , 42.19267 ,
        41.177753, 40.258003, 40.178585, 40.83267 , 41.054337, 41.336586,
        41.210423, 41.468918, 41.441006, 41.64458 , 41.09084 ]
D = np.array(D) # turn into numpy so can be vector calcs
D = D / 1000
TIME = range(1958, 2017)

# TotalFWF = [1016.9741697416974, 1018.081180811808, 1034.6863468634685
# , 1025.830258302583, 969.3726937269373, 898.5239852398523, 900.7380073800738
# , 866.420664206642, 874.169741697417, 908.4870848708488, 912.9151291512915, 915.1291512915129
# , 891.8819188191882, 863.0996309963099, 846.4944649446494, 860.8856088560885
# , 829.8892988929889, 850.9225092250922, 859.7785977859778, 852.0295202952029
# , 855.350553505535, 884.1328413284133, 891.8819188191882, 884.1328413284133
# , 907.380073800738, 919.5571955719557, 883.0258302583026, 896.309963099631
# , 939.4833948339484, 940.590405904059, 951.6605166051661, 992.619926199262
# , 946.1254612546126, 949.4464944649446, 938.3763837638376, 937.2693726937268
# , 910.7011070110701, 949.4464944649446, 971.5867158671587, 990.4059040590405
# , 988.1918819188191, 1028.0442804428044, 1072.3247232472324, 1103.3210332103322
# , 1134.3173431734317, 1183.0258302583024, 1191.8819188191883, 1219.5571955719556
# , 1225.0922509225093, 1231.7343173431734, 1259.409594095941, 1302.5830258302583
# , 1339.1143911439115, 1300.3690036900368, 1315.8671586715868, 1278.228782287823
# , 1290.4059040590405, 1271.5867158671585, 1323.6162361623617]
# TotalFWF = np.array(TotalFWF)
#%% plot
color_list = ['lightgray', 'lightgray', 'lightgray', 'lightgray', 'lightgray',
              'white', 'lightgray', 'lightgray', 'white', 'lightgray']
edgecolor_list = ['None', 'None', 'None', 'None', 'None',
              'k', 'None', 'None', 'k', 'None']
fig = plt.figure()
gs = fig.add_gridspec(1, 2, wspace=0.1, width_ratios=(4, 1))
axes = gs.subplots(sharex=False, sharey=False)
# fig, ax = plt.subplots()
rects = axes[0].bar(x,
                freshwater_sorted,
                color=color_list,
                yerr=[freshwater_std_sorted_lower,freshwater_std_sorted_upper], # for one-sided error bar
                capsize=2,
                edgecolor=edgecolor_list,
                zorder=3)

# Plot observed FWF
ax2 = axes[0].twiny()
# ax2.plot(Enderlin2014_df['Year'], Enderlin2014_df['Discharge (mSv)'], '-o',
#          markerfacecolor='None', markeredgecolor='k', color='k')
ax2.plot(TIME, D*12/31.6, '-o', markerfacecolor='None', markeredgecolor='k',
         color='k') # 31.6 is the conversion from km3/yr to mSV
# ax2.plot(TIME, TotalFWF/31.6, '-ok', markersize=2)
# axes[1].scatter([0.5, 0.5, 0.5, 0.5, 0.5],
#                 [15, 18, 28, 54, 8])

axes[1].scatter(2100, 9.925/1000, marker='^', facecolor='#f6bd60', edgecolor='#f6bd60', clip_on = False,  zorder=10) # Muntjewerf ice discharge RCP 8.5
axes[1].scatter(2100, 7.5975/1000, marker='^', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge RCP 8.5
axes[1].scatter(2100-20, 9.2774/1000, marker='s', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge RCP 4.5
axes[1].scatter(2100+15, 9.8119/1000, marker='v', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge RCP 2.6
axes[1].scatter(2200, 4.4287/1000, marker='^', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2200 RCP 8.5
axes[1].scatter(2200, 8.0556/1000, marker='s', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2200 RCP 4.5
axes[1].scatter(2200, 9.5446/1000, marker='v', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2200 RCP 2.6
axes[1].scatter(2300, 3.8178/1000, marker='^', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2300 RCP 8.5
axes[1].scatter(2300, 8.0175/1000, marker='s', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2300 RCP 4.5
axes[1].scatter(2300, 9.8882/1000, marker='v', facecolor='#1d3557', edgecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 ice discharge 2300 RCP 2.6

#%% Beautification
axes[0].set(yscale='log')
axes[1].set(yscale='log')
axes[0].set_ylabel('Ice discharge (Sv)')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels_sorted)
axes[0].set_xlim(left=-0.75)
axes[0].set_ylim((ylim_lower, ylim_upper))
axes[1].set_ylim((ylim_lower, ylim_upper))
axes[1].yaxis.set_ticklabels([])
# ax.tick_params(right=True, labelright=True)
axes[0].text(5.7, 4.6e2/1000, 'Year')
# axes[0].grid(False, axis='x')

# ax2.grid(False)

# set up a twiny for Gt/yr in the right panel
ax_gt = axes[0].twinx()
ax_gt.set_ylim((ylim_lower/1e12*830*365.25*24*60*60*1e6, ylim_upper/1e12*830*365.25*24*60*60*1e6))
ax_gt.set(yscale='log')
ax_gt.yaxis.set_ticklabels([])

# set up a twiny for Gt/yr in the left panel
ax_gt = axes[1].twinx()
ax_gt.set_ylim((ylim_lower/1e12*830*365.25*24*60*60*1e6, ylim_upper/1e12*830*365.25*24*60*60*1e6))
ax_gt.set(yscale='log')
ax_gt.set_ylabel('Ice discharge (Gt/yr)')

axes[1].xaxis.tick_top()

axes[1].grid(False, axis='x')

# set up fake legends
legend_elements = [Line2D([0], [0], marker='^', color='None', label='RCP 8.5',
                          markerfacecolor='w', markeredgecolor='k', markersize=7),
                   Line2D([0], [0], marker='s', color='None', label='RCP 4.5',
                          markerfacecolor='w', markeredgecolor='k', markersize=7),
                   Line2D([0], [0], marker='v', color='None', label='RCP 2.6',
                          markerfacecolor='w', markeredgecolor='k', markersize=7),
                   ]
axes[1].legend(handles=legend_elements, loc='upper center', fontsize='small',
               columnspacing=1)

# add height text
axes[0].bar_label(rects, fmt='%.3f')

# sns.despine()
fig.set_size_inches(7,5)
# plt.tight_layout()

# plt.savefig('Freshwater_flux_this_study_max_mSV.png',dpi=500)
plt.savefig('../figures/Figure_4.pdf')
# plt.savefig('Ice_discharge_this_study_max_SV_projections_talk.pdf')