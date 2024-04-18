#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 12:14:18 2022

@author: zhou
"""

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.legend_handler import HandlerPatch
import pandas as pd
from matplotlib.lines import Line2D

sns.set(font='Arial',palette='husl',style='ticks')

labels=np.array(['MacAyeal 1993', 'Rahmstorf 1995',#'Dowdeswell et al. 1995','
        'Manabe & Stouffer 1995', 'Manabe & Stouffer 1997',
        'Marshall & Clarke 1997', #'Roberts et al. 2014',
        'Hemming 2004', 'Fairbanks 1989',
        'Roche et al. 2004', 'Labeyrie et al. 1995', ])

# calculations can be found in OneNote
# Page "Literature Ffwf"
freshwater = np.array([0.16, 0.06,#0.016, 
              1, 0.1,
              0.03, #0.04,
              1.25, 0.44,
              0.29, 0.04375])
# freshwater = freshwater * 1000

freshwater_sorted = np.take(freshwater, np.argsort(freshwater))
labels_sorted = np.take(labels, np.argsort(freshwater))
model_or_no_sorted = [True, #True, True, 
                      False, True, True, True, False,
                      False, True, False]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

ylim_lower = 1e-2
ylim_upper = 2e0

#%% plot
fig = plt.figure()
gs = fig.add_gridspec(1, 2, wspace=0.1, width_ratios=(4, 1))
axes = gs.subplots(sharex=False, sharey=True)

rects = axes[0].bar(x[model_or_no_sorted],
                freshwater_sorted[model_or_no_sorted],
                color='white',
                edgecolor='k',
                linestyle='--',
                label='Model-based')
rects2 = axes[0].bar(x[[not a for a in model_or_no_sorted]],
                freshwater_sorted[[not a for a in model_or_no_sorted]],
                color='white',
                edgecolor='k',
                label='Observation-based')
axes[0].set_ylim((ylim_lower, ylim_upper))
# rect = axes[0].bar(x, freshwater_sorted)

# denote which HE the est is on
# axes[0].text(0, 0.019*1000, 'H1/2', verticalalignment='bottom', horizontalalignment='center')
axes[0].text(3, 0.013, 'YD', horizontalalignment='center')
axes[0].text(5, 0.013, 'H4', horizontalalignment='center')
axes[0].text(8, 0.013, 'H4', horizontalalignment='center')

axes[1].scatter(2100, 15/1000, marker='s', facecolor='#f5cac3', clip_on = False,  zorder=10) # Golledge 2019 RCP 4.5
axes[1].scatter(2100, 18/1000, marker='^', facecolor='#f5cac3', clip_on = False,  zorder=10) # Golledge 2019 RCP 8.5
axes[1].scatter(2100+15, 28/1000, marker='^', facecolor='#f28482', clip_on = False,  zorder=10) # Goelzer RCP 8.5
axes[1].scatter(2100, 54/1000, marker='^', facecolor='#f6bd60', clip_on = False,  zorder=10) # Muntjewerf RCP 8.5
axes[1].scatter(2100+15, 43/1000, marker='v', facecolor='#a8dadc', clip_on = False,  zorder=10) # Lenaerts 2015 RCP 2.6
axes[1].scatter(2100, 62/1000, marker='^', facecolor='#a8dadc', clip_on = False,  zorder=10) # Lenaerts 2015 RCP 8.5
axes[1].scatter(2200, 77/1000, marker='^', facecolor='#a8dadc', clip_on = False,  zorder=10) # Lenaerts 2015 2200 RCP 8.5
axes[1].scatter(2200, 40/1000, marker='v', facecolor='#a8dadc', clip_on = False,  zorder=10) # Lenaerts 2015 2200 RCP 2.6

axes[1].scatter(2100, 47.31/1000, marker='^', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 RCP 8.5
axes[1].scatter(2100, 32.71/1000, marker='s', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 RCP 4.5
axes[1].scatter(2100, 28.15/1000, marker='v', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 RCP 2.6
axes[1].scatter(2200, 83.68/1000, marker='^', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2200 RCP 8.5
axes[1].scatter(2200, 34.69/1000, marker='s', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2200 RCP 4.5
axes[1].scatter(2200, 25.93/1000, marker='v', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2200 RCP 2.6
axes[1].scatter(2300, 102.17/1000, marker='^', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2300 RCP 8.5
axes[1].scatter(2300, 37.66/1000, marker='s', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2300 RCP 4.5
axes[1].scatter(2300, 27.21/1000, marker='v', facecolor='#1d3557', clip_on = False,  zorder=10) # Vizcaino 2015 2300 RCP 2.6

#%% Plot observed FWF from Yang 2015
######## Testing #########
# # Bamber 2018
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
# TotalFWF
# TIME = range(1958, 2017)
# ax2 = axes[0].twiny()
# circle_patch = ax2.plot(TIME, TotalFWF/31.6/1000, '-', markerfacecolor='k', markeredgecolor='None',
#           color='k', label='Observed GrIS freshwater flux') # 31.6 is the conversion from km3/yr to mSV
###########################

TotalFWF = pd.read_excel('Yang2016.xlsx')
ax2 = axes[0].twiny()
circle_patch = ax2.plot(TotalFWF['Year'], TotalFWF['mSV']/1000, '-o', markerfacecolor='k', markeredgecolor='None',
          color='k', label='Observed GrIS freshwater flux') # 31.6 is the conversion from km3/yr to mSV

#%% Beautification

plt.yscale('log')
axes[0].set_ylabel('Freshwater flux (Sv)')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels_sorted,
                   rotation=45,ha='right')
# axes[0].set_yticks([10, 20, 30, 40, 50,
#                     60, 70, 80, 90, 100,
#                     200, 300, 400, 500, 600,
#                     700, 800, 900, 1000, 2000])
# set a zombie artist to create legend with a diff color than actually plotted
model_patch = mpatches.Patch(facecolor='white',
                              edgecolor='k',
                              linestyle='--',
                              label='Model-based reconstruction')
obs_patch = mpatches.Patch(facecolor='white',
                           edgecolor='k',
                           linestyle='-',
                           label='Observation-based reconstruction')

plt.legend(handles=[model_patch, obs_patch],# circle_patch[0]],
           fontsize='x-small',
           loc='upper left')

# set up a twiny for Gt/yr in the right panel
ax_gt = axes[0].twinx()
ax_gt.set_ylim((ylim_lower/1e12*1000*365.25*24*60*60*1e6, ylim_upper/1e12*1000*365.25*24*60*60*1e6))
ax_gt.set(yscale='log')
ax_gt.yaxis.set_ticklabels([])

# set up a twiny for Gt/yr in the left panel
ax_gt = axes[1].twinx()
ax_gt.set_ylim((ylim_lower/1e12*1000*365.25*24*60*60*1e6, ylim_upper/1e12*1000*365.25*24*60*60*1e6))
ax_gt.set(yscale='log')
ax_gt.set_ylabel('Freshwater flux (Gt/yr)')

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

# axes[0].legend()
axes[0].grid(False, axis='x')
ax2.grid(False)
axes[0].text(5, 3.5e0, 'Year')
axes[1].xaxis.tick_top()
axes[1].grid(False, axis='x')

# add height text
axes[0].bar_label(rects, fmt='%.2g')
axes[0].bar_label(rects2, fmt='%.2g')

fig.set_size_inches(7, 5)
# axes[0].tight_layout()
# plt.savefig('Freshwater_flux_literature_mSV_Gt.png',dpi=500)
plt.savefig('../figures/Figure_1.pdf',bbox_inches='tight')