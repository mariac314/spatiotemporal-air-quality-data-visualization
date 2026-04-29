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
run-spatiotemporal-analysis # This runs using pre-determined inputs, which can be changed as seen in the example code
```
## Functions
1. ```read_icartt_data_files(data_file_name, coord_file_name)```
  - Purpose: Load the data and coordinate icartt files
  - Input: data file name, coordinate file name (these files are in the same folder as the py files)
  - Output: Confirmation that the files are loaded by printing data type and headers
2. ```select_VOC(VOC_name, data)```
  - Purpose: Extract the desired VOC from the dataset and explore its variable properties
  - Input: VOC name (as seen in the data file headers) and dataset from function 1 (read_icartt_data_files())
  - Output: an array of the VOC that can be used for plotting - will also display missing data value flags, data units, and data type and shape
3. ```time_align(VOC_dict, time_data, time_coord, lat, lon)```
  - Purpose: Time-align the VOC and coordinate datasets to prevent future alignment and shape errors
  - Input: Dictionary of VOC names and corresponding arrays (from select_VOC()), time arrays from the VOC and coordinate datasets, and latitude and longitude from the coordinate dataset
  - Output: Dataframe that has the aligned time points and corresponding coordinates and select VOCs
4. ```plot_VOC_map(VOC_name, VOC, lat, lon)```
  - Purpose: plot selected VOCs on corresponding coordinate points and view mixing ratio along the route
  - Input: VOC name, and VOC data, lat, lon from the time-aligned dataframe (Function 3)
  - Output: A map with the VOC mixing ratio plotted on top of the route coordinates
5. ```plot_peaks_above_baseline(VOC, VOC_name, time)```
  - Purpose: Observe VOC spikes and plumes by viewing the time series of the data
  - Input: VOC name, and VOC data and time from the time-aligned dataframe (Function 3)
  - Output: A plot of the VOC time series with plume points and background points differentiated by color
    
## Example Usage 
```python
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

# Add target VOC(s) for time alignment with coordinate data
target_VOCs = {'Methanol': methanol}

combined_data = time_align(target_VOCs, time_data, time_coord, lat, lon)

VOC_plot = combined_data.Methanol # This can be whatever VOC you want
time_plot = combined_data.Time 
lat_plot = combined_data.Latitude
lon_plot = combined_data.Longitude
VOC_name = "Methanol"

# Plot the VOC map and time series
plot_VOC_map(VOC_name, VOC_plot, lat_plot, lon_plot) 
plot_peaks_above_baseline(VOC_plot, VOC_name, time_plot)
```
