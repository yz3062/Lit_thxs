# Lit_thxs

This is a public repository containing the data and code used to analyze a compilation of North Atlantic sedimentary uranium series records to reconstruct the ice discharges during Heinrich events. The flowchart below illustrates the workflow for generating publication-ready figures from the raw data.

![Flowchart](https://github.com/yz3062/Lit_thxs/blob/master/Flowchart.png)

## Guide to the data files

**python/literature_Thxs_compilation_mass_flux_updated.xlsx** - compilation of time series of uranium series isotope records, including new data generated from three cores - EW9303-GGC31 (50° 34.2’ N, 46° 21’W, water depth 1796 m), DY081-GVY005 (58° 36.6’ N, 43° 46.8’ W, water depth 1907 m), and V30-100 (44° 7.02’ N, 32° 30’ W, water depth 3519 m).

**python/Yang2016.xlsx** -- freshwater flux data (Yang et al., 2016) (doi: 10.1038/ncomms10525)

**python/MF_H1_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx** - Spatially interpolated surge mass flux during Heinrich event 1, calculated by subtracting the 1-kyr average of mass flux during Heinrich event 1 by the Last Glacial Maximum (18-21 ka) mass flux. The spatial interpolation is done with Data Interpolating Variational Analysis (DIVA) in Ocean Data View (ODV). Locations without data are marked with -1E+10.

**python/MF_H1_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx** - Spatially interpolated surge mass flux during Heinrich event 1, calculated by subtracting the 2-kyr average of mass flux during Heinrich event 1 by the Last Glacial Maximum (18-21 ka) mass flux. The spatial interpolation is done with Data Interpolating Variational Analysis (DIVA) in Ocean Data View (ODV). Locations without data are marked with -1E+10.

**python/MF_H1_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx** - Spatially interpolated surge mass flux during Heinrich event 1, calculated by subtracting the 4-kyr average of mass flux during Heinrich event 1 by the Last Glacial Maximum (18-21 ka) mass flux. The spatial interpolation is done with Data Interpolating Variational Analysis (DIVA) in Ocean Data View (ODV). Locations without data are marked with -1E+10.

**python/MF_H1_DIVA_from_ODV_HE_max_interglacial_diff.xlsx** - Spatially interpolated surge mass flux during Heinrich event 1, calculated by subtracting the maximum mass flux during Heinrich event 1 by the last two interglacials (0-12 ka and 70-125 ka) mass flux. The spatial interpolation is done with Data Interpolating Variational Analysis (DIVA) in Ocean Data View (ODV). Locations without data are marked with -1E+10.

**python/MF_H1_DIVA_from_ODV_HE_max_LGM_diff.xlsx** - Spatially interpolated surge mass flux during Heinrich event 1, calculated by subtracting the maximum mass flux during Heinrich event 1 by the Last Glacial Maximum (18-21 ka) mass flux. The spatial interpolation is done with Data Interpolating Variational Analysis (DIVA) in Ocean Data View (ODV). Locations without data are marked with -1E+10.

The following files adhere to the same naming conventions of Heinrich event 1, but are for other events (Heinrich events 2-6, HQ, and Younger Dryas):

python/MF_H2_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_H2_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_H2_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_H2_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_H2_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_H3_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_H3_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_H3_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_H3_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_H3_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_H4_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_H4_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_H4_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_H4_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_H4_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_H5_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_H5_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_H5_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_H5_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_H5_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_H6_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_H6_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_H6_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_H6_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_H6_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_HQ_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_HQ_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_HQ_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_HQ_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_HQ_DIVA_from_ODV_HE_max_LGM_diff.xlsx

python/MF_YD_DIVA_from_ODV_HE_1kyr_mean_LGM_diff.xlsx

python/MF_YD_DIVA_from_ODV_HE_2kyr_mean_LGM_diff.xlsx

python/MF_YD_DIVA_from_ODV_HE_4kyr_mean_LGM_diff.xlsx

python/MF_YD_DIVA_from_ODV_HE_max_interglacial_diff.xlsx

python/MF_YD_DIVA_from_ODV_HE_max_LGM_diff.xlsx

The following folders store the shapefiles of ice sheet extents during various time steps of the last glacial periods, used in Figure 3. Each folder has a "readme" file with the data source and citation information.

**python/Eurasian_ice_sheets_shapefiles**

**python/Laurentide_and_Eurasia_shapefiles**

**python/Laurentide_shapefiles**

**python/Quaternary_ice_sheets_shapefiles**

## Guide to the Python scripts
**Surge_mass_flux_to_csv_for_ODV.py** - generates the CSV files as input for Ocean Data View (ODV) to interpolate to gridded fields of surge mass flux, which is used to calculate the flux of ice discharges.

**Mean_mass_flux_to_csv_for_ODV.py** - generates the CSV files as input for Ocean Data View (ODV) to interpolate to gridded fields of mean mass flux, which is used to calculate the volume of ice discharges by multiplying time.

**Freshwater_flux_literature_SV_projections.py** - generates Figure 1.

**lit_thxs_maps_freshwater_HE_max_LGM_diff_SV.py** - generates Figure 3 and calculates the spatially integrated ice discharges during each event.

**Ice_discharge_this_study_max_SV_projections.py** - uses the printing output from **lit_thxs_maps_freshwater_HE_max_LGM_diff_SV.py** and generates Figure 4.

**lit_thxs_raw_mass_flux_original_age.py** - generates Figure S5 and exports the mass flux 1-kyr running mean (black line) as **Mass_flux_running_mean.csv**

**dataset_fetching_func.py** - worker script with functions to properly read in the compilation.
