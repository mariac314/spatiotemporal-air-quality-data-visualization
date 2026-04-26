import icartt 
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px 

# Import the data processing and plotting functions
from data_loading_functions import read_icartt_data_files
from data_loading_functions import select_VOC
from data_loading_functions import time_align
from plotting_functions import plot_VOC_map
from plotting_functions import plot_peaks_above_baseline

# Analysis setup - these inputs can be modified depending on your interests and what files you want to look at 
# USOS
data_file_name = 'USOS_PTR_MobileLab_20240803.ict'
coord_file_name = 'USOS_MetNav_MobileLab_20240803.ict'

# AEROMMA
#data_file_name = 'AEROMMA_NOAAPTR_DC8_20230822.ict'
#coord_file_name = 'AEROMMA_MetNav_DC8_20230822.ict'

def main():
    data, coords = read_icartt_data_files(data_file_name, coord_file_name)
    time_data = data.data['Time_Start']
    # Select whatever VOCs you are interested in from the dataset - here I am selecting three different hazardous air pollutants (HAPs)
    methanol = select_VOC('CH3OH_NOAAPTR_ppbv', data)
    benzene = select_VOC('Benzene_NOAAPTR_ppbv', data)
    toluene = select_VOC('Toluene_NOAAPTR_ppbv', data)

    # Get coordinates and time - naming varies between USOS and AEROMMA coordinate files
    try:
        lat = coords.data['GPS_Lat_deg']
        lon = coords.data['GPS_Lon_deg']

    except ValueError:
       try:
          lat = coords.data['Latitude']
          lon = coords.data['Longitude']
          # I had to add this mask because the AEROMMA coordinate file does not use -9999 for missing data, but -999900000
          lat[lat<-9999] = np.nan
          lon[lon<-9999] = np.nan
       except ValueError:
           return None 

    time_coord = coords.data['Time_Start']

    # Add target VOCs for time alignment with coordinate data
    target_VOCs = {
    'Methanol': methanol,
    'Benzene': benzene,
    'Toluene': toluene
    }
    combined_data = time_align(target_VOCs, time_data, time_coord, lat, lon)

    VOC_plot = combined_data.Methanol # This can be whatever VOC you want
    time_plot = combined_data.Time 
    lat_plot = combined_data.Latitude
    lon_plot = combined_data.Longitude

    # Provide the name of the VOC your are plotting for label purposes
    VOC_name = "Methanol"
    # This will generate a map with the VOC mixing ratio plotted along the measurement route
    plot_VOC_map(VOC_name, VOC_plot, lat_plot, lon_plot) 
    #
    plot_peaks_above_baseline(VOC_plot, VOC_name, time_plot)

if __name__ == "__main__":
    main()