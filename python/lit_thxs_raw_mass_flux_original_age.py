#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:23:08 2020

@author: yuxinzhou

Note: runs in conda env cartopy18 but not cartopy_update -- something about
pandas update that broke groupby. Numeric_only=True?
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dataset_fetching_func

sns.set(font='Arial', palette='husl', style='ticks')
lit_thxs_pd = dataset_fetching_func.fetch_df(include_unpublished = False,
                                             aU_or_MF='MF',
                                             age_as_index=True,
                                             sort_age=True,
                                             )

fig = plt.figure()
ax = plt.gca()
for key, grp in lit_thxs_pd.groupby(['Core']):
    grp = grp.dropna(subset=['Mass Flux (g/cm2kyr)'])
    grp.plot(ax=ax, kind='line', y='Mass Flux (g/cm2kyr)', sharex=True,
             legend=False, label='', color='gray',alpha=0.5)

# plot a rolling mean (window=1) of all lines. Notice the unit of timedelta is
# days since year needs to be integers.
# lit_thxs_pd = dataset_fetching_func.fetch_nontropical_NA_df(False)
# plt.plot(lit_thxs_pd.index-0.5, lit_thxs_pd
#          .set_index(pd.to_timedelta(lit_thxs_pd.index.values, unit='d'))
#          .rolling('1d')
#          .mean()['Mass Flux (g/cm2kyr)'], color='C0', label='Non-tropical NA')
# lit_thxs_pd = dataset_fetching_func.fetch_tropical_NA_df(False)
# plt.plot(lit_thxs_pd.index-0.5, lit_thxs_pd
#          .set_index(pd.to_timedelta(lit_thxs_pd.index.values, unit='d'))
#          .rolling('1d')
#          .mean()['Mass Flux (g/cm2kyr)'], color='C1', label='Tropical NA')
# lit_thxs_pd = dataset_fetching_func.fetch_arctic_df(False)
# plt.plot(lit_thxs_pd.index-0.5, lit_thxs_pd
#          .set_index(pd.to_timedelta(lit_thxs_pd.index.values, unit='d'))
#          .rolling('1d')
#          .mean()['Mass Flux (g/cm2kyr)'], color='C2', label='Arctic')
plt.plot(lit_thxs_pd.index-0.5, lit_thxs_pd
          .set_index(pd.to_timedelta(lit_thxs_pd.index.values, unit='d'))
          .rolling('1d')
          .mean()['Mass Flux (g/cm2kyr)'],
          label='1 kyr running mean',
          color='k',
          zorder=3)
running_mean = lit_thxs_pd.set_index(
    pd.to_timedelta(
        lit_thxs_pd.index.values, unit='d')).rolling(
            '1d').mean()['Mass Flux (g/cm2kyr)']
            
# Marking HEs
for i, j in zip([16.1, 24.4, 31.7, 38.4, 48, 61, 67.5],
                ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HQ']):
    plt.axvline(x=i, linestyle='--', zorder=2)
    plt.text(i,51,j,horizontalalignment='center',color='C0')

# plot infinite mass flux as triangles on top
plt.legend(loc=1)
inf_mass_flux_ages = [45.3846, 46.1538, 46.9231, 52.3077, 61.5385, 250, 38,
                      23.4921, 36.362, 37.6619, 53.0769, 54.6154, 56.1538, 60,
                      62.3077, 45.8108, 45]
plt.plot(inf_mass_flux_ages, [49] * len(inf_mass_flux_ages),
         '^', markersize=3,color='k')
# plt.yscale('log')
plt.ylim((-4,50))
plt.xlim((0, 150))
plt.ylabel('Mass flux (g/cm2kyr)')
sns.despine()
plt.tight_layout()
# fig.set_size_inches(6, 4)
plt.savefig('lit_thxs_raw_mass_flux_original_age.png',dpi=700)
# plt.savefig('lit_thxs_raw_mass_flux_original_age.pdf')

#%% export running_mean
output_frame = pd.DataFrame({'Age (ka)': lit_thxs_pd.index-0.5,
                             'Mass Flux (g/cm2kyr)': running_mean.values})