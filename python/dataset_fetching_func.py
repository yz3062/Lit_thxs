#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:13:49 2020

@author: zhou
"""

import pandas as pd
import numpy as np


def fetch_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.

    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
        	Whether to set age as index.

    sort_age : boolean
        	Whether to sort index.
        
    exclude_abnormal_234 : boolean
        Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    if exclude_abnormal_234 is True:
        lit_thxs_pd = pd.read_excel(
            '../literature_Thxs_compilation_234U_lippold2009_anomaly_removed.xlsx',
            sheet_name='Master')
    else:
        if aU_or_MF == 'aU':
            lit_thxs_pd = pd.read_excel(
                '../literature_Thxs_compilation_auth_U_no_XRF.xlsx',
                sheet_name='Master')
            # At Bermuda Rise, two cores are practically from the same location
            # Replace one's info with the other so the two can merge
            lit_thxs_pd = lit_thxs_pd.replace('KNR31 GPC5', 'ODP 172-1063')
            lit_thxs_pd = lit_thxs_pd.replace(-57.615, -57.62)
            lit_thxs_pd = lit_thxs_pd.replace(33.687, 33.68)
            lit_thxs_pd = lit_thxs_pd.replace(4583, 4584.0)
        elif aU_or_MF == 'MF':
            lit_thxs_pd = pd.read_excel(
                '../literature_Thxs_compilation_mass_flux.xlsx',
                sheet_name='Master')
        else:
            raise ValueError("This function has added a parameter aU_or_MF. Specify that input.")
    if include_unpublished is False:
        lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Citation'] != 'Unpublished']
    if age_as_index is True:
        lit_thxs_pd.set_index('Age (ka BP)', inplace=True)
    # This step is important if include_unpublished is False
    # because Monte Carlo age index will have gaps if index not reset
    else:
        lit_thxs_pd.reset_index(inplace=True)
    if sort_age is True:
        lit_thxs_pd.sort_index(inplace=True)
    return lit_thxs_pd

def fetch_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
        	Whether to set age as index.

    sort_age : boolean
        	Whether to sort index.

    exclude_abnormal_234 : boolean
        Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] <= 65]
    return lit_thxs_pd

def fetch_arctic_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
        	Whether to set age as index.

    sort_age : boolean
        	Whether to sort index.

    exclude_abnormal_234 : boolean
        Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] > 65]
    return lit_thxs_pd

def fetch_nontropical_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Latitude'] <= 65)
                              & (lit_thxs_pd['Latitude'] >= 23.5)]
    return lit_thxs_pd

def fetch_nontropical_west_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Latitude'] <= 65)
                              & (lit_thxs_pd['Latitude'] >= 23.5)
                              & (lit_thxs_pd['Longitude'] <= -40)]
    return lit_thxs_pd

def fetch_nontropical_east_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Latitude'] <= 65)
                              & (lit_thxs_pd['Latitude'] >= 23.5)
                              & (lit_thxs_pd['Longitude'] >= -40)]
    return lit_thxs_pd

def fetch_tropical_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] < 23.5]
    return lit_thxs_pd

def fetch_west_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Latitude'] <= 65)
                              & (lit_thxs_pd['Longitude'] <= -40)]
    return lit_thxs_pd

def fetch_east_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                           aU_or_MF=aU_or_MF,
                           age_as_index=age_as_index,
                           sort_age=sort_age,
                           exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Latitude'] <= 65)
                              & (lit_thxs_pd['Longitude'] >= -40)]
    return lit_thxs_pd

def fetch_MAR_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    return lit_thxs_pd

def fetch_arctic_MAR_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] >= 65]
    return lit_thxs_pd

def fetch_east_MAR_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Longitude']>=-30) &
                              (lit_thxs_pd['Core'] != 'V22-182') |
                              (lit_thxs_pd['Core'] == 'KN207-2-GGC3')]
    return lit_thxs_pd

def fetch_west_MAR_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Longitude']<=-30) &
                              (lit_thxs_pd['Core'] != 'KN207-2-GGC3') |
                              (lit_thxs_pd['Core'] == 'V22-182')]
    return lit_thxs_pd

def fetch_MAR_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] <= 70]
    return lit_thxs_pd

def fetch_MAR_east_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] <= 70]
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Longitude']>=-30) &
                          (lit_thxs_pd['Core'] != 'V22-182') |
                          (lit_thxs_pd['Core'] == 'KN207-2-GGC3')]
    return lit_thxs_pd

def fetch_MAR_west_NA_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['aU MAR (ug/cm2kyr)'])
    lit_thxs_pd = lit_thxs_pd[lit_thxs_pd['Latitude'] <= 70]
    lit_thxs_pd = lit_thxs_pd[(lit_thxs_pd['Longitude']<=-30) &
                          (lit_thxs_pd['Core'] != 'KN207-2-GGC3') |
                          (lit_thxs_pd['Core'] == 'V22-182')]
    return lit_thxs_pd

def fetch_aU_2sigma_df(include_unpublished, aU_or_MF, age_as_index=True, sort_age=True,
             exclude_abnormal_234=False):
    """


    Parameters
    ----------
    include_unpublished : boolean
        Whether to inlcude unpublished data.
        
    aU_or_MF : string
        'aU' returns original cores included in the aU study
        'MF' returns original cores included in the MF study
    
    age_as_index : boolean
    	Whether to set age as index.

    sort_age : boolean
    	Whether to sort index.

    exclude_abnormal_234 : boolean
    Whether to exclude abnormal 234 uncertainty (mainly in Lippold 2009)

    Returns
    -------
    lit_thxs_pd : pandas.Dataframe
        A pandas dataframe containing the literature Thxs dataset.

    """
    lit_thxs_pd = fetch_df(include_unpublished=include_unpublished,
                       aU_or_MF=aU_or_MF,
                       age_as_index=age_as_index,
                       sort_age=sort_age,
                       exclude_abnormal_234=exclude_abnormal_234)
    lit_thxs_pd = lit_thxs_pd.dropna(subset=['Auth U (ppm) 2 sigma'])
    return lit_thxs_pd