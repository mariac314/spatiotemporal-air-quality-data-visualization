# spatiotemporal-air-quality-data-visualization
Final project that maps spatiotemporal volatile organic compound (VOC) measurements and explores time series and enhancements for data collected on mobile and aircraft platforms.


## GitHub cloning and install instructions
```python
# Clone this repository
git clone https://github.com/mariac314/spatiotemporal-air-quality-data-visualization.git

# Move into the folder (where the toml file is)
cd spatiotemporal-air-quality-data-visualization

# Install in editable mode
pip install -e .

# Can Python import it from anywhere? 
cd /tmp

# Run it from the command line
run-spatiotemporal-analysis # This runs using pre-determined inputs, which can be changed as seen below
```
## Example Usage 
```python
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


data, coords = read_icartt_data_files(data_file_name, coord_file_name)
time_data = data.data['Time_Start']
# Select whatever VOCs you are interested in from the dataset - here I am selecting methanol
methanol = select_VOC('CH3OH_NOAAPTR_ppbv', data)

# Assign coordinates
lat = coords.data['GPS_Lat_deg']
lon = coords.data['GPS_Lon_deg']
time_coord = coords.data['Time_Start']

# Add target VOCs for time alignment with coordinate data
target_VOCs = {'Methanol': methanol}

combined_data = time_align(target_VOCs, time_data, time_coord, lat, lon)

VOC_plot = combined_data.Methanol # This can be whatever VOC you want
time_plot = combined_data.Time 
lat_plot = combined_data.Latitude
lon_plot = combined_data.Longitude

VOC_name = "Methanol"
# This will generate a map with the VOC mixing ratio plotted along the measurement route
plot_VOC_map(VOC_name, VOC_plot, lat_plot, lon_plot) 
# This will generate the time series highlighting VOC enhancements above background
plot_peaks_above_baseline(VOC_plot, VOC_name, time_plot)
```
