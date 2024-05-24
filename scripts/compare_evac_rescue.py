import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import rasterio
from rasterio.transform import from_origin
import pyproj

import folium
from folium.plugins import HeatMap
from functools import partial


data_dir_nono = '../Results/No-evac_NO-rescue'
nono_counts = pd.DataFrame(columns=['time', 'count'])


for filename in os.listdir(data_dir_nono):
    if filename.endswith(".csv"):
        time_str = '2021' +filename.split('_')[2] + '_' + filename.split('_')[3].split('.')[0]
        time = datetime.strptime(time_str, '%Y%m%d_%H')
        
        data = pd.read_csv(os.path.join(data_dir_nono, filename))
              
        count = data.shape[0]
              
        print(type(nono_counts))
        nono_counts = pd.concat([nono_counts, pd.DataFrame({'time': [time], 'count': [count]})], ignore_index=True)

nono_counts = nono_counts.sort_values(by='time')


# Directory of inputs
data_dir_noyes = '../Results/No-evac_OK-rescue'
noyes_counts = pd.DataFrame(columns=['time', 'count'])

for filename in os.listdir(data_dir_noyes):
    
    if filename.endswith(".csv"):
        
        time_str = '2021' + filename.split('_')[1] + '_' + filename.split('_')[2].split('.')[0]
        time = datetime.strptime(time_str, '%Y%m%d_%H')
        
        data = pd.read_csv(os.path.join(data_dir_noyes, filename))
        
        count = data.shape[0]
        
        noyes_counts = pd.concat([noyes_counts, pd.DataFrame({'time': [time], 'count': [count]})], ignore_index=True)


noyes_counts = noyes_counts.sort_values(by='time')
start_date = datetime.strptime('2021_0901_00', '%Y_%m%d_%H')
end_date = max(nono_counts['time'].max(), noyes_counts['time'].max())  
all_dates = pd.date_range(start_date, end_date, freq='H')
all_dates_df = pd.DataFrame(all_dates, columns=['time'])

nono_counts = pd.merge(all_dates_df, nono_counts, on='time', how='left')
noyes_counts = pd.merge(all_dates_df, noyes_counts, on='time', how='left')


nono_counts['count'].fillna(0, inplace=True)
noyes_counts['count'].fillna(0, inplace=True)


data_dir1 = ''
obs = pd.read_csv(os.path.join(data_dir1, '../Data/obs_raritanriver_gateheight.csv'))

obs_timef = [datetime.strptime(t, '%m/%d/%Y %H:%M') for t in obs['datetime']]

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'

ax1.set_ylabel('Number of buildings', color=color)
ax1.plot(nono_counts['time'], nono_counts['count'], color='tab:red', label='Non-Evacuable and Unrescuable')
ax1.plot(noyes_counts['time'], noyes_counts['count'], color=color, label='Non-Evacuable but rescuable')
ax1.tick_params(axis='y', labelcolor=color)
plt.grid()
ax2 = ax1.twinx() 


peak_time = obs_timef[obs['navd88'].idxmax()]
ax1.axvline(x=peak_time, color='k', linestyle='--')
color = 'tab:green'

ax2.set_ylabel('Observed Water Elevation', color=color)  
ax2.plot(obs_timef, obs['navd88']/3.28084, color=color, label="Observed Water Elevation (meter @NAVD88)")
ax2.tick_params(axis='y', labelcolor=color)
start_date = datetime.strptime('2021-09-01 00:00', '%Y-%m-%d %H:%M')
end_date = datetime.strptime('2021-09-03 02:00', '%Y-%m-%d %H:%M')
ax1.set_xlim([start_date, end_date])

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(0, 1))

fig.tight_layout()  
plt.savefig("time-series.png", dpi=300)
plt.show()


