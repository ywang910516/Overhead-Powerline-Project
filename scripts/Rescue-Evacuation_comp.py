# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:34:51 2023

@author: Yifan Wang
"""

#deal with no-rescue-no-evacuation data
#deal with rescuable-no-evacuation data

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Directory where your files are stored
data_dir_nono = '../Results/No-evac_NO-rescue'
nono_counts = pd.DataFrame(columns=['time', 'count'])


for filename in os.listdir(data_dir_nono):
    
    if filename.endswith(".csv"):
        time_str = filename.split('_')[2] + '_' + filename.split('_')[3].split('.')[0]
        time = datetime.strptime(time_str, '%m%d_%H')
        data = pd.read_csv(os.path.join(data_dir_nono, filename))
        count = data.shape[0]
        nono_counts = nono_counts.append({'time': time, 'count': count}, ignore_index=True)

nono_counts = nono_counts.sort_values(by='time')


data_dir_noyes = '../Results/No-evac_OK-rescue'

noyes_counts = pd.DataFrame(columns=['time', 'count'])

for filename in os.listdir(data_dir_noyes):
    if filename.endswith(".csv"):
        time_str = filename.split('_')[1] + '_' + filename.split('_')[2].split('.')[0]
        time = datetime.strptime(time_str, '%m%d_%H')
        data = pd.read_csv(os.path.join(data_dir_noyes, filename))
        count = data.shape[0]

        noyes_counts = noyes_counts.append({'time': time, 'count': count}, ignore_index=True)

noyes_counts = noyes_counts.sort_values(by='time')

plt.figure(figsize=(10, 6))
plt.plot(nono_counts['time'], nono_counts['count'])
plt.plot(noyes_counts['time'], noyes_counts['count'])
plt.xlabel('Time')
plt.ylabel('Number of flooded buildings')
plt.title('Time series of evacuation and rescue availability')
plt.legend('')
plt.show()










