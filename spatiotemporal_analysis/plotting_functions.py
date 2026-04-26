import icartt 
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px 

def plot_VOC_map(VOC_name, VOC, lat, lon):
    """
    Purpose: plot selected VOCs on corresponding coordinate points and view mixing ratio along the route
    Input: 
        VOC_name: The name of the selected VOC, as seen in the data header
        VOC: The VOC selected from the time_aligned dataframe
        lat: latitude from the coordinate file (time-aligned)
        lon: longitude from the coordinate file (time-aligned)
    Output: A map with the VOC mixing ratio plotted on top of the route coordinates
    Source: https://plotly.com/python/tile-map-layers/
    """
    plotting_df = pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'VOC': VOC,
        'VOC_size': VOC
    })

    fig = px.scatter_map(plotting_df.dropna(), lat="lat", lon="lon", size="VOC", size_max=45, color="VOC") # Need dropna() so size works
    
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text=f'{VOC_name} (ppb)',
                side="right"  
            ),
        )
    )
    fig.update_layout(
        map_style="white-bg",
        map_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(map_bounds={"west": min(lon)-0.05, "east": max(lon)+0.05, "south": min(lat)-0.05, "north": max(lat)+0.05}) # Source: https://plotly.com/python/tile-map-layers/
    fig.write_html('VOC_mixing_ratio_map.html') # Source: https://plotly.com/python/interactive-html-export/
    fig.show()
    return fig

def plot_peaks_above_baseline(VOC, VOC_name, time):
    """
    Purpose: Observe VOC spikes and plumes by viewing the time series of the data
    Input: 
        VOC_name: The name of the selected VOC, as seen in the data header
        VOC: The VOC selected from the time_aligned dataframe
        time: The time from the time_aligned dataframe
    Output: A plot of the VOC time series (mixing ratios are in log scale due to data spanning several 
            orders of magnitude) with plume points and background points differentiated by color
    """

    rolling_std = VOC.rolling(window=300).std() # Choose baseline region based on lowest rolling 5-minute standard deviation 
    baseline_end = rolling_std.idxmin() # This gives the last value in the region
    baseline_std = rolling_std.min()
    baseline_start = baseline_end - 300
    baseline_region = VOC[baseline_start:baseline_end] # Select the VOC points corresponding to the baseline region

    # Calculate the baseline mean + 3*standard deviations - for a non-normal distribution, about 90% of the data fall within this range
    # data that fall outside of this range are considered outliers or in the case of VOCs, emission events
    baseline_mean = baseline_region.mean()
    three_times_std = 3*baseline_std
    baseline_mean_with_noise = baseline_mean + three_times_std
    print(f"The baseline mean + 3σ is {baseline_mean_with_noise:.2f} ppb")

    VOC_below_baseline = VOC.copy() # Need to copy so I don't end up with an array that is entirely nans 
    VOC_below_baseline[VOC_below_baseline>baseline_mean_with_noise] = np.nan
    
    VOC_above_baseline = VOC.copy()
    VOC_above_baseline[VOC_above_baseline<=baseline_mean_with_noise] = np.nan


    date = pd.Timestamp('2024-08-03') # Change this based on the date in the file name
    time_format = pd.to_timedelta(time, unit='s')
    time_mdt = time_format - pd.Timedelta(hours=6) # UTC is 6 hours ahead of MDT
    time_clean = date + time_mdt

    print(time_clean)
    plt.scatter(time_clean, VOC_above_baseline, 2, 'blue', label='Above baseline')
    plt.scatter(time_clean, VOC_below_baseline, 2, 'orange', label='Below baseline')
    plt.axhline(y = baseline_mean_with_noise, color='black', linestyle='--', label='Baseline mean + 3$\sigma$')
    plt.ylabel(f'{VOC_name} (ppb)')
    plt.xlabel('Time (MDT)')
    plt.title(f'{VOC_name} Enhancements Above Background')
    plt.yscale('log')
    plt.legend(markerscale=5)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.savefig('VOC_mixing_ratio_time_series.png', dpi = 600, bbox_inches='tight')
    plt.show()
    return ax

