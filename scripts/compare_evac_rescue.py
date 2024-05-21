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







data_dir1 = '../Data/'
data_dir_nono = '../Results/No-evac_NO-rescue'

buildings_location = pd.read_csv(os.path.join(data_dir1, 'Non_res_dur_location2.csv'))

all_flooded_locations = pd.DataFrame(columns=['POINT_X', 'POINT_Y'])
POINT_X=buildings_location['POINT_X']
POINT_Y=buildings_location['POINT_Y']

for filename in os.listdir(data_dir_nono):
    
    if filename.endswith(".csv") and 'route_all' in filename:                
        data = pd.read_csv(os.path.join(data_dir_nono, filename))
        flooded_locations = pd.merge(data, buildings_location, how='inner', left_on='Missing Code', right_on='Id')
        all_flooded_locations = pd.concat([all_flooded_locations, flooded_locations[['POINT_X', 'POINT_Y']]], ignore_index=True)

colors = [(1, 1, 1, 0), (1, 0, 0, 1)]  
cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)


fig, ax = plt.subplots(figsize=(10, 6))


counts, xedges, yedges, im = plt.hist2d(all_flooded_locations['POINT_X']/3.28084, all_flooded_locations['POINT_Y']/3.28084, bins=10, cmap=cmap, alpha=0.5)

x_bin_width = xedges[1] - xedges[0]
y_bin_height = yedges[1] - yedges[0]

for i in range(counts.shape[0]):
    for j in range(counts.shape[1]):
        if counts[i, j] > 0:  
            plt.text(xedges[i] + x_bin_width/2, yedges[j] + y_bin_height/2, str(int(counts[i, j])), ha='center', va='center')

plt.colorbar(label='Hours')
plt.xlabel('X')
plt.ylabel('Y')
ax.set_xlim(141000, 144000)
ax.set_ylim(188750, 191000)
plt.title('Spatial Distribution of Buildings * Hours (Non-Evacuable and Unrescuable)')
plt.savefig("Aggregate spatial distribution_nono.png", dpi=300)
plt.show()


data_dir1 = '../Data/'
data_dir_nono = '../Results/No-evac_OK-rescue'

buildings_location = pd.read_csv(os.path.join(data_dir1, 'Non_res_dur_location2.csv'))


all_flooded_locations = pd.DataFrame(columns=['POINT_X', 'POINT_Y'])


for filename in os.listdir(data_dir_nono):
    
    if filename.endswith(".csv") and 'route' in filename:        
        
        data = pd.read_csv(os.path.join(data_dir_nono, filename))
            
        flooded_locations = pd.merge(data, buildings_location, how='inner', left_on='In rescue but not evac', right_on='Id')

        all_flooded_locations = pd.concat([all_flooded_locations, flooded_locations[['POINT_X', 'POINT_Y']]], ignore_index=True)

colors = [(1, 1, 1, 0), (1, 0, 0, 1)]  
cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)

fig, ax = plt.subplots(figsize=(10, 6))
plt.hist2d(all_flooded_locations['POINT_X']/3.28084, all_flooded_locations['POINT_Y']/3.28084, bins=10, cmap=cmap, alpha=0.5)
plt.colorbar(label='Hours')
plt.xlabel('X')
plt.ylabel('Y')
ax.set_xlim(141000, 144000)
ax.set_ylim(188750, 191000)
plt.title('Spatial Distribution of Buildings * Hours (Non-Evacuable but rescuable)')
plt.savefig("Aggregate spatial distribution_noyes.png", dpi=300)
plt.show()






data_dir1 = '../Data/'
data_dir_nono = '../Results/No-evac_NO-rescue'


buildings_location = pd.read_csv(os.path.join(data_dir1, 'Non_res_dur_location2.csv'))


all_flooded_locations = pd.DataFrame(columns=['POINT_X', 'POINT_Y'])
POINT_X=buildings_location['POINT_X']
POINT_Y=buildings_location['POINT_Y']


for filename in os.listdir(data_dir_nono):
    
    if filename.endswith(".csv") and 'route_all' in filename:        
        
        data = pd.read_csv(os.path.join(data_dir_nono, filename))
        
        
        flooded_locations = pd.merge(data, buildings_location, how='inner', left_on='Missing Code', right_on='Id')
        
        
        all_flooded_locations = pd.concat([all_flooded_locations, flooded_locations[['POINT_X', 'POINT_Y']]], ignore_index=True)

colors = [(1, 1, 1, 0), (1, 0, 0, 1)]  
cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)


fig, ax = plt.subplots(figsize=(10, 6))

counts, xedges, yedges, im = plt.hist2d(all_flooded_locations['POINT_X']/3.28084, all_flooded_locations['POINT_Y']/3.28084, bins=10, cmap=cmap, alpha=0.5)


x_bin_width = xedges[1] - xedges[0]
y_bin_height = yedges[1] - yedges[0]
for i in range(counts.shape[0]):
    for j in range(counts.shape[1]):
        if counts[i, j] > 0:  
            plt.text(xedges[i] + x_bin_width/2, yedges[j] + y_bin_height/2, str(int(counts[i, j])), ha='center', va='center')

plt.colorbar(label='Hours')
plt.xlabel('X')
plt.ylabel('Y')
ax.set_xlim(141000, 144000)
ax.set_ylim(188750, 191000)
plt.title('Spatial Distribution of Buildings * Hours (Non-Evacuable and Unrescuable)')
plt.savefig("Aggregate spatial distribution_nono.png", dpi=300)


