import icartt 
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 

def read_icartt_data_files(data_file_name, coord_file_name):
    """ 
    Purpose: Load the data and coordinate icartt files
    Input: data file name, coordinate file name - these need to be in the same folder as the python analysis files
    Output: Confirmation that the files are loaded by printing data type and headers
    """

    data = icartt.Dataset(pathlib.Path(data_file_name))
    coords = icartt.Dataset(pathlib.Path(coord_file_name))
 
    print(f"Data file type: {type(data)}")
    print(f"Coordinate file type: {type(coords)}")
    print(f"Data file headers: {[x for x in data.variables]}") # This lets you know which VOCs are included and how their names are formatted
    print(f"Coordinate file headers: {[x for x in coords.variables]}")
    return data, coords

def select_VOC(VOC_name, data):
    """ 
    Purpose: Extract the desired VOC from the dataset and explore its variable properties
    Input: VOC name (as seen in the data file headers) and dataset from function 1 (read_icartt_data_files())
    Output: an array of the VOC that can be used for plotting - will also display missing data value flags, data units, and data type and shape
    """
    VOC_variable_info = data.variables[VOC_name]
    select_VOC = data.data[VOC_name]
    select_VOC[select_VOC < 0] = np.nan 
    print(f"Missing data values: {VOC_variable_info.miss}") # -9999 is converted to nan automatically
    print(f"Data units: {VOC_variable_info.units}")
    print(f"VOC data type: {type(select_VOC)}")
    print(f"VOC data shape: {select_VOC.shape}")
    return select_VOC

def time_align(VOC_dict, time_data, time_coord, lat, lon):
    """
    Purpose: Time-align the VOC and coordinate datasets to prevent future alignment and shape errors
    Input: Dictionary of VOC names and corresponding arrays (from select_VOC()), time arrays from 
           the VOC and coordinate datasets, and latitude and longitude from the coordinate dataset
    Output: Dataframe that has the aligned time points and corresponding coordinates and select VOCs
    """
    VOC_data = {'Time': time_data}
    for VOC_name, VOC_array in VOC_dict.items():
        VOC_data[VOC_name] = VOC_array

    coord_data = {'Time': time_coord,
                'Latitude': lat,
                'Longitude': lon}

    VOC_df = pd.DataFrame(VOC_data)
    coord_df = pd.DataFrame(coord_data)

    combined_data = pd.merge(coord_df, VOC_df,  on='Time') # Source for using pd.merge(): https://www.geeksforgeeks.org/pandas/python-pandas-merging-joining-and-concatenating/?ysclid=mnbyz36yop687525772
    #combined_data = combined_data.dropna()
    print(f"Combined data layout: {combined_data.head()}")
    print(f'Combined data shape: {combined_data.shape}')
    return combined_data

