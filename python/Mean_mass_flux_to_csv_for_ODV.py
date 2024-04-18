#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:23:15 2022

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import numpy.ma as ma
import dataset_fetching_func
import seaborn as sns
from matplotlib import ticker

sns.set(font='Arial',palette='husl',style='ticks')

lit_thxs_pd = dataset_fetching_func.fetch_df(include_unpublished = False,
                                             aU_or_MF='MF',
                                             age_as_index = False,
                                             sort_age = False,
                                             exclude_abnormal_234 = False,
                                             )
# numeric_only: https://stackoverflow.com/questions/69653925/wrong-number-of-items-passed-1-placement-implies-3-pandas-1-1-5
# change the age intervals below to average 1, 2, and 4 kyrs
YD = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=11.2) & (lit_thxs_pd['Age (ka BP)']<=12.2)].groupby('Core').mean(numeric_only=True)
H1 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=15.6) & (lit_thxs_pd['Age (ka BP)']<=16.6)].groupby('Core').mean(numeric_only=True)
H2 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=23.9) & (lit_thxs_pd['Age (ka BP)']<=24.9)].groupby('Core').mean(numeric_only=True)
H3 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=31.2) & (lit_thxs_pd['Age (ka BP)']<=32.2)].groupby('Core').mean(numeric_only=True)
H4 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=37.9) & (lit_thxs_pd['Age (ka BP)']<=38.9)].groupby('Core').mean(numeric_only=True)
H5 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=47.5) & (lit_thxs_pd['Age (ka BP)']<=48.5)].groupby('Core').mean(numeric_only=True)
H6 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=60.5) & (lit_thxs_pd['Age (ka BP)']<=61.5)].groupby('Core').mean(numeric_only=True)
HQ = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=67) & (lit_thxs_pd['Age (ka BP)']<=68)].groupby('Core').mean(numeric_only=True)

#%% LGM
LGM = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=18) &
                  (lit_thxs_pd['Age (ka BP)']<=21)].groupby('Core').mean()
# HE - LGM
YD['Mass Flux (g/cm2kyr)'] = YD['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H1['Mass Flux (g/cm2kyr)'] = H1['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H2['Mass Flux (g/cm2kyr)'] = H2['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H3['Mass Flux (g/cm2kyr)'] = H3['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H4['Mass Flux (g/cm2kyr)'] = H4['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H5['Mass Flux (g/cm2kyr)'] = H5['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
H6['Mass Flux (g/cm2kyr)'] = H6['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
HQ['Mass Flux (g/cm2kyr)'] = HQ['Mass Flux (g/cm2kyr)'] - LGM['Mass Flux (g/cm2kyr)']
diff_df = pd.concat([YD,
            H1,
            H2,
            H3,
            H4,
            H5,
            H6,
            HQ])
diff_df.dropna(subset=['Mass Flux (g/cm2kyr)'], inplace=True)
diff_df.to_csv('lit_thxs_HE_1kyr_mean_LGM_dff.csv')

#%% Interglacials
interglacial = lit_thxs_pd[((lit_thxs_pd['Age (ka BP)']>=0) &
                            (lit_thxs_pd['Age (ka BP)']<=10)) |
                            ((lit_thxs_pd['Age (ka BP)']>=70) &
                            (lit_thxs_pd['Age (ka BP)']<=125))].groupby('Core').mean()
# HE - interglacials
YD['Mass Flux (g/cm2kyr)'] = YD['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H1['Mass Flux (g/cm2kyr)'] = H1['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H2['Mass Flux (g/cm2kyr)'] = H2['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H3['Mass Flux (g/cm2kyr)'] = H3['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H4['Mass Flux (g/cm2kyr)'] = H4['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H5['Mass Flux (g/cm2kyr)'] = H5['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
H6['Mass Flux (g/cm2kyr)'] = H6['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
HQ['Mass Flux (g/cm2kyr)'] = HQ['Mass Flux (g/cm2kyr)'] - interglacial['Mass Flux (g/cm2kyr)']
diff_df = pd.concat([YD,
            H1,
            H2,
            H3,
            H4,
            H5,
            H6,
            HQ])
diff_df.dropna(subset=['Mass Flux (g/cm2kyr)'], inplace=True)
diff_df.to_csv('lit_thxs_HE_max_interglacial_dff.csv')
