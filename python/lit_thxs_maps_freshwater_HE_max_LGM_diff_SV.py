#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:56:58 2022

@author: zhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# cartopy must be version 0.18
# the newer version 0.21 messes up the maps projection
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
YD = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=11) & (lit_thxs_pd['Age (ka BP)']<=13)].groupby('Core').mean(numeric_only=True)
H1 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=16) & (lit_thxs_pd['Age (ka BP)']<=18)].groupby('Core').mean(numeric_only=True)
H2 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=23) & (lit_thxs_pd['Age (ka BP)']<=25)].groupby('Core').mean(numeric_only=True)
H3 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=30) & (lit_thxs_pd['Age (ka BP)']<=32)].groupby('Core').mean(numeric_only=True)
H4 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=37) & (lit_thxs_pd['Age (ka BP)']<=39)].groupby('Core').mean(numeric_only=True)
H5 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=46) & (lit_thxs_pd['Age (ka BP)']<=48)].groupby('Core').mean(numeric_only=True)
H6 = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=59) & (lit_thxs_pd['Age (ka BP)']<=61)].groupby('Core').mean(numeric_only=True)
HQ = lit_thxs_pd[(lit_thxs_pd['Age (ka BP)']>=66) & (lit_thxs_pd['Age (ka BP)']<=68)].groupby('Core').mean(numeric_only=True)
# set a common range for all scatters, so one colorbar covers all
vmin = 0
vmax = 12e-10

star_size = 30

def MF_to_freshwater(array):
    """
    

    Parameters
    ----------
    array : numpy.Array
        DESCRIPTION.

    Returns
    -------
    numpy.Array
        Freshwater flux in mSv/km2.

    """
    # 0.00589: from IRD weight [g] to iceberg water weight [g]
    # 0.83e6: from iceberg water weight [g] to iceberg volume [m3]
    # 1e10: from cm2 to km2
    # (1000*365*24*60*60): from time [kyr] to time [s]
    # 1e-6: from flux [m3/s] to Sv [10e6 m3/s]
    return array / 0.00589 / 0.83e6 * 1e10 / (1000*365.25*24*60*60) * 1e-6

#%% YD
fig = plt.figure()

# ax1 = plt.subplot(2,4,1,projection=ccrs.Orthographic(central_longitude=-40,
#                                                       central_latitude=50))
ax1 = plt.subplot(2,4,1,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax1 = plt.subplot(2,4,1,projection=ccrs.NearsidePerspective(central_longitude=-40,
#                                                       central_latitude=50,
#                                                       satellite_height=35785831))

# ax1.set_extent([-100, 40, -5, 90])
# ax1_extent = ax1.get_extent(crs=ccrs.PlateCarree())  # for later to set H5-HQ extent
# ax1.set_global()
ax1.coastlines(resolution='50m')
ax1.gridlines(draw_labels=False)
ax1.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
fname = 'Eurasian_ice_sheets_shapefiles/DATED1_TimeSlices_shp/TS12_mc.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax1.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Laurentide_shapefiles/WGS84/ice012500/ice012500.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='gray')
ax1.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('YD')

# DIVA 
YD_DIVA_pd = pd.read_excel('MF_YD_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(YD_DIVA_pd['Longitude'])
lat = np.unique(YD_DIVA_pd['Latitude'])
YD_DIVA = YD_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
YD_DIVA = MF_to_freshwater(YD_DIVA)
# Should chheck if the first value is always masked
YD_DIVA_ma = ma.masked_equal(YD_DIVA,YD_DIVA[0,0])
#show only ocean data
locations = np.c_[YD_DIVA_pd['Longitude'].values,
                  YD_DIVA_pd['Latitude'].values] # concatenate
YD_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
YD_mask = YD_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
YD_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
YD_mask[I,J]=True
YD_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
YD_DIVA_arctic_unmasked_ma = ma.array(YD_DIVA_ma,mask=YD_mask)
YD_DIVA_arctic_unmasked_ma = YD_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
YD_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
YD_mask[I,J]=True
YD_DIVA_ma = ma.array(YD_DIVA_ma,mask=YD_mask)
# mask negative values
YD_DIVA_ma = YD_DIVA_ma.clip(min=0)
# YD_DIVA_ma = ma.masked_less(YD_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct1 = ax1.contourf(xx,yy,YD_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax1.scatter(YD['Longitude'].values,
               YD['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())
#%% H1
ax2 = plt.subplot(2,4,2,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax2.set_global()
ax2.coastlines(resolution='50m')
ax2.gridlines(draw_labels=False)
ax2.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
fname = 'Eurasian_ice_sheets_shapefiles/DATED1_TimeSlices_shp/TS17_mc.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax2.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Laurentide_shapefiles/WGS84/ice017000/ice017000.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='gray')
ax2.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('H1')

# DIVA 
H1_DIVA_pd = pd.read_excel('MF_H1_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H1_DIVA_pd['Longitude'])
lat = np.unique(H1_DIVA_pd['Latitude'])
H1_DIVA = H1_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
# Convert to freshwater
H1_DIVA = MF_to_freshwater(H1_DIVA)
# Should chheck if the first value is always masked
H1_DIVA_ma = ma.masked_equal(H1_DIVA,H1_DIVA[0,0])
#show only ocean data
locations = np.c_[H1_DIVA_pd['Longitude'].values,
                  H1_DIVA_pd['Latitude'].values] # concatenate
H1_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H1_mask = H1_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H1_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H1_mask[I,J]=True
H1_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H1_DIVA_arctic_unmasked_ma = ma.array(H1_DIVA_ma,mask=H1_mask)
H1_DIVA_arctic_unmasked_ma = H1_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H1_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H1_mask[I,J]=True
H1_DIVA_ma = ma.array(H1_DIVA_ma,mask=H1_mask)
# mask negative values
H1_DIVA_ma = H1_DIVA_ma.clip(min=0)
# H1_DIVA_ma = ma.masked_less(H1_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct2 = ax2.contourf(xx,yy,H1_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax2.scatter(H1['Longitude'].values,
               H1['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% H2
ax3 = plt.subplot(2,4,3,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax3.set_global()
ax3.coastlines(resolution='50m')
ax3.gridlines(draw_labels=False)
ax3.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
fname = 'Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='gray')
ax3.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('H2')

# DIVA 
H2_DIVA_pd = pd.read_excel('MF_H2_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H2_DIVA_pd['Longitude'])
lat = np.unique(H2_DIVA_pd['Latitude'])
H2_DIVA = H2_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
H2_DIVA = MF_to_freshwater(H2_DIVA)
# Should chheck if the first value is always masked
H2_DIVA_ma = ma.masked_equal(H2_DIVA,H2_DIVA[0,0])
#show only ocean data
locations = np.c_[H2_DIVA_pd['Longitude'].values,
                  H2_DIVA_pd['Latitude'].values] # concatenate
H2_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H2_mask = H2_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H2_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H2_mask[I,J]=True
H2_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H2_DIVA_arctic_unmasked_ma = ma.array(H2_DIVA_ma,mask=H2_mask)
H2_DIVA_arctic_unmasked_ma = H2_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H2_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H2_mask[I,J]=True
H2_DIVA_ma = ma.array(H2_DIVA_ma,mask=H2_mask)
# mask negative values
H2_DIVA_ma = H2_DIVA_ma.clip(min=0)
# H2_DIVA_ma = ma.masked_less(H2_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct3 = ax3.contourf(xx,yy,H2_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax3.scatter(H2['Longitude'].values,
               H2['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% H3
ax4 = plt.subplot(2,4,4,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax4.set_global()
ax4.coastlines(resolution='50m')
ax4.gridlines(draw_labels=False)
ax4.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
# fname = '../../python/Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
# shape_feature = ShapelyFeature(Reader(fname).geometries(),
#                                 ccrs.PlateCarree(), facecolor='gray')
# ax4.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Quaternary_ice_sheets_shapefiles/30 ka/hypothesised ice-sheet reconstructions/30ka_best_estimate.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax4.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('H3')

# DIVA
H3_DIVA_pd = pd.read_excel('MF_H3_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H3_DIVA_pd['Longitude'])
lat = np.unique(H3_DIVA_pd['Latitude'])
H3_DIVA = H3_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
H3_DIVA = MF_to_freshwater(H3_DIVA)
# Should chheck if the first value is always masked
H3_DIVA_ma = ma.masked_equal(H3_DIVA,H3_DIVA[0,0])
#show only ocean data
locations = np.c_[H3_DIVA_pd['Longitude'].values,
                  H3_DIVA_pd['Latitude'].values] # concatenate
H3_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H3_mask = H3_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H3_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H3_mask[I,J]=True
H3_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H3_DIVA_arctic_unmasked_ma = ma.array(H3_DIVA_ma,mask=H3_mask)
H3_DIVA_arctic_unmasked_ma = H3_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H3_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H3_mask[I,J]=True
H3_DIVA_ma = ma.array(H3_DIVA_ma,mask=H3_mask)
# mask negative values
H3_DIVA_ma = H3_DIVA_ma.clip(min=0)
# H3_DIVA_ma = ma.masked_less(H3_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct4 = ax4.contourf(xx,yy,H3_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax4.scatter(H3['Longitude'].values,
               H3['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% H4
ax5 = plt.subplot(2,4,5,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax5.set_global()
ax5.coastlines(resolution='50m')
ax5.gridlines(draw_labels=False)
ax5.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
# fname = '../../python/Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
# shape_feature = ShapelyFeature(Reader(fname).geometries(),
#                                 ccrs.PlateCarree(), facecolor='gray')
# ax5.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Quaternary_ice_sheets_shapefiles/40 ka/hypothesised ice-sheet reconstructions/40ka_best_estimate.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax5.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('H4')

# DIVA 
H4_DIVA_pd = pd.read_excel('MF_H4_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H4_DIVA_pd['Longitude'])
lat = np.unique(H4_DIVA_pd['Latitude'])
H4_DIVA = H4_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
H4_DIVA = MF_to_freshwater(H4_DIVA)
# Should chheck if the first value is always masked
H4_DIVA_ma = ma.masked_equal(H4_DIVA,H4_DIVA[0,0])
#show only ocean data
locations = np.c_[H4_DIVA_pd['Longitude'].values,
                  H4_DIVA_pd['Latitude'].values] # concatenate
H4_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H4_mask = H4_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H4_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H4_mask[I,J]=True
H4_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H4_DIVA_arctic_unmasked_ma = ma.array(H4_DIVA_ma,mask=H4_mask)
H4_DIVA_arctic_unmasked_ma = H4_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H4_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H4_mask[I,J]=True
H4_DIVA_ma = ma.array(H4_DIVA_ma,mask=H4_mask)
# mask negative values
H4_DIVA_ma = H4_DIVA_ma.clip(min=0)
# H4_DIVA_ma = ma.masked_less(H4_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct5 = ax5.contourf(xx,yy,H4_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax5.scatter(H4['Longitude'].values,
               H4['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% H5
ax6 = plt.subplot(2,4,6,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# # A bug prevents set_extext from working with non_rect projections
# ax6.set_extent((-90, 180, -19.84705795647886, 90), crs=ccrs.PlateCarree())
# ax6.set_global()
ax6.coastlines(resolution='50m')
ax6.gridlines(draw_labels=False)
ax6.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
# fname = '../../python/Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
# shape_feature = ShapelyFeature(Reader(fname).geometries(),
#                                 ccrs.PlateCarree(), facecolor='gray')
# ax6.add_feature(shape_feature, zorder=3, edgecolor="None")
ax6.add_feature(shape_feature, zorder=3, edgecolor="None")


plt.title('H5')

# DIVA 
H5_DIVA_pd = pd.read_excel('MF_H5_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H5_DIVA_pd['Longitude'])
lat = np.unique(H5_DIVA_pd['Latitude'])
H5_DIVA = H5_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
H5_DIVA = MF_to_freshwater(H5_DIVA)
# Should chheck if the first value is always masked
H5_DIVA_ma = ma.masked_equal(H5_DIVA,H5_DIVA[0,0])
#show only ocean data
locations = np.c_[H5_DIVA_pd['Longitude'].values,H5_DIVA_pd['Latitude'].values] # concatenate
H5_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H5_mask = H5_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H5_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H5_mask[I,J]=True
H5_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H5_DIVA_arctic_unmasked_ma = ma.array(H5_DIVA_ma,mask=H5_mask)
H5_DIVA_arctic_unmasked_ma = H5_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H5_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H5_mask[I,J]=True
H5_DIVA_ma = ma.array(H5_DIVA_ma,mask=H5_mask)
# mask negative values
H5_DIVA_ma = H5_DIVA_ma.clip(min=0)
# H5_DIVA_ma = ma.masked_less(H5_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct6 = ax6.contourf(xx,yy,H5_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax6.scatter(H5['Longitude'].values,
               H5['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% H6
ax7 = plt.subplot(2,4,7,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax7.set_extent(ax1_extent, crs=ccrs.PlateCarree())
# ax7.set_global()
ax7.coastlines(resolution='50m')
ax7.gridlines(draw_labels=False)
ax7.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
# fname = '../../python/Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
# shape_feature = ShapelyFeature(Reader(fname).geometries(),
#                                 ccrs.PlateCarree(), facecolor='gray')
# ax7.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Quaternary_ice_sheets_shapefiles/MIS 4/hypothesised ice-sheet reconstructions/MIS4_best_estimate.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax7.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('H6')

# DIVA 
H6_DIVA_pd = pd.read_excel('MF_H6_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(H6_DIVA_pd['Longitude'])
lat = np.unique(H6_DIVA_pd['Latitude'])
H6_DIVA = H6_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
H6_DIVA = MF_to_freshwater(H6_DIVA)
# Should chheck if the first value is always masked
H6_DIVA_ma = ma.masked_equal(H6_DIVA,H6_DIVA[0,0])
#show only ocean data
locations = np.c_[H6_DIVA_pd['Longitude'].values,H6_DIVA_pd['Latitude'].values] # concatenate
H6_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
H6_mask = H6_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
H6_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
H6_mask[I,J]=True
H6_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
H6_DIVA_arctic_unmasked_ma = ma.array(H6_DIVA_ma,mask=H6_mask)
H6_DIVA_arctic_unmasked_ma = H6_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
H6_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
H6_mask[I,J]=True
H6_DIVA_ma = ma.array(H6_DIVA_ma,mask=H6_mask)
# mask negative values
H6_DIVA_ma = H6_DIVA_ma.clip(min=0)
# H6_DIVA_ma = ma.masked_less(H6_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct7 = ax7.contourf(xx,yy,H6_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax7.scatter(H6['Longitude'].values,
               H6['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% HQ
ax8 = plt.subplot(2,4,8,projection=ccrs.LambertAzimuthalEqualArea(central_longitude=-40,
                                                      central_latitude=50))
# ax8.set_extent(ax1_extent, crs=ccrs.PlateCarree())
# ax8.set_global()
ax8.coastlines(resolution='50m')
ax8.gridlines(draw_labels=False)
ax8.add_feature(cfeature.LAND, zorder=2, edgecolor='None')
# fname = '../../python/Laurentide_and_Eurasia_shapefiles/lgm/lgm.shp'
# shape_feature = ShapelyFeature(Reader(fname).geometries(),
#                                 ccrs.PlateCarree(), facecolor='gray')
# ax8.add_feature(shape_feature, zorder=3, edgecolor="None")
fname = 'Quaternary_ice_sheets_shapefiles/MIS 4/hypothesised ice-sheet reconstructions/MIS4_best_estimate.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.LambertAzimuthalEqualArea(central_latitude=90), facecolor='gray')
ax8.add_feature(shape_feature, zorder=3, edgecolor="None")

plt.title('HQ')

# DIVA 
HQ_DIVA_pd = pd.read_excel('MF_HQ_DIVA_from_ODV_HE_max_LGM_diff.xlsx',
                           index_col=None,header=0)
lon = np.unique(HQ_DIVA_pd['Longitude'])
lat = np.unique(HQ_DIVA_pd['Latitude'])
HQ_DIVA = HQ_DIVA_pd['Mass flux'].values.reshape(len(lat),len(lon))
HQ_DIVA = MF_to_freshwater(HQ_DIVA)
# Should chheck if the first value is always masked
HQ_DIVA_ma = ma.masked_equal(HQ_DIVA,HQ_DIVA[0,0])
#show only ocean data
locations = np.c_[HQ_DIVA_pd['Longitude'].values,HQ_DIVA_pd['Latitude'].values] # concatenate
HQ_mask = np.zeros(len(locations), dtype=bool)
# mask Hudson Bay, Mediterranean etc
HQ_mask = HQ_mask.reshape(len(lat),len(lon))
# diagonal slicing and rectangular slicing shouldn't be mixed
# source: https://stackoverflow.com/questions/34646839/numpy-multi-dimensional-slicing-with-multiple-boolean-arrays
I,J = np.ix_(lat<65,lon<-80)
HQ_mask[I,J]=True
I,J = np.ix_(lat<65,lon>10)
HQ_mask[I,J]=True
HQ_mask[lat<-5,:]=True
# Arctic unmasked for complete freshwater accounting
HQ_DIVA_arctic_unmasked_ma = ma.array(HQ_DIVA_ma,mask=HQ_mask)
HQ_DIVA_arctic_unmasked_ma = HQ_DIVA_arctic_unmasked_ma.clip(min=0)
# Addtional conditions to take out part of Arctic
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon<-60)
HQ_mask[I,J]=True
I,J = np.ix_(np.logical_and(lat<85, lat>60),lon>60)
HQ_mask[I,J]=True
HQ_DIVA_ma = ma.array(HQ_DIVA_ma,mask=HQ_mask)
# mask negative values
HQ_DIVA_ma = HQ_DIVA_ma.clip(min=0)
# HQ_DIVA_ma = ma.masked_less(HQ_DIVA_ma, 0)
xx, yy = np.meshgrid(lon, lat)
ct8 = ax8.contourf(xx,yy,HQ_DIVA_ma,vmin=vmin,vmax=vmax,cmap='viridis',
                 transform=ccrs.PlateCarree(),zorder=1,levels=np.linspace(vmin, vmax, 50),
                   extend='both')#,levels=[0,0.5,1,1.5])

sc = ax8.scatter(HQ['Longitude'].values,
               HQ['Latitude'].values,
               vmin=vmin,vmax=vmax,c='orangered',s=2,
               transform=ccrs.PlateCarree())

#%% Ice discharge flux

# Ice discharge (Sv) in NA
# 5500 km2 is the area of a grid cell
YD_freshwater_flux_NA = YD_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H1_freshwater_flux_NA = H1_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H2_freshwater_flux_NA = H2_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H3_freshwater_flux_NA = H3_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H4_freshwater_flux_NA = H4_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H5_freshwater_flux_NA = H5_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
H6_freshwater_flux_NA = H6_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500
HQ_freshwater_flux_NA = HQ_DIVA_arctic_unmasked_ma[np.logical_and(lat>20,lat<70),:].sum() * 5500

print('YD ice discharge: ' + str(YD_freshwater_flux_NA))
print('H1 ice discharge: ' + str(H1_freshwater_flux_NA))
print('H2 ice discharge: ' + str(H2_freshwater_flux_NA))
print('H3 ice discharge: ' + str(H3_freshwater_flux_NA))
print('H4 ice discharge: ' + str(H4_freshwater_flux_NA))
print('H5 ice discharge: ' + str(H5_freshwater_flux_NA))
print('H6 ice discharge: ' + str(H6_freshwater_flux_NA))
print('HQ ice discharge: ' + str(HQ_freshwater_flux_NA))
#%% beautify
# textbox
freshwater = np.array([4, 16, 28, 3,
                       130, 26, 10, 14])
freshwater = freshwater/1000
axes = [ax1, ax2, ax3, ax4,
        ax5, ax6, ax7, ax8]
for i in range(8):
    axes[i].text(0.05, 0.05, f'{freshwater[i]:.3f}'+' Sv',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor='w', edgecolor='gray', alpha=0.5),
                 transform=axes[i].transAxes)
    
# colorbar
fig.subplots_adjust(left=0.05,right=0.8)
cbar_ax = fig.add_axes([0.85, 0.07, 0.02, 0.86])
cbar = fig.colorbar(ct5, cax=cbar_ax, ticks=np.linspace(vmin, vmax, 11))
cbar.set_label(r'Ice discharge per unit area (${}^\mathrm{Sv}$/${}_\mathrm{km}{}^\mathrm{2}$)')

# font size change
# import matplotlib.pylab as pylab
# params = {'legend.fontsize': 8,
#          'axes.labelsize': 8,
#          'axes.titlesize': 8,
#          'xtick.labelsize': 8,
#          'ytick.labelsize': 8}
# pylab.rcParams.update(params)

fig.set_size_inches(8, 4)
# plt.savefig('lit_thxs_maps_freshwater_HE_max_LGM_diff_SV.png', dpi=700)
plt.savefig('../figures/Figure_3.pdf')