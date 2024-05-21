# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:57:49 2023

@author: Yifan
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv("../Data/Non_res_dur_location2.csv")


# Coordinates of the center of the town
center_x = 467335.356
center_y = 622399.016


df["Relative_X"] = df["POINT_X"] - center_x
df["Relative_Y"] = df["POINT_Y"] - center_y

angles = np.arctan2(df["Relative_Y"], df["Relative_X"])

angles_deg = np.degrees(angles)
angles_deg = (angles_deg +360) %360 
num_bins = int(360 / 45)

# Create the rose plot
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)
ax.set_rlabel_position(90)
ax.set_title("Rescue Service Interruption Durations Across Different Directions", pad=20)

# Define the duration sections and their corresponding colors
duration_sections = [0, 5, 10, 15, 20, 26]
colors = ['blue', 'orange', 'green', 'red', 'purple']

# Initialize an array to store the height of each stacked bar
bottom = np.zeros(num_bins)

# Loop through each duration section and plot the histogram for each bin
for i in range(len(duration_sections) - 1):
    section_start = duration_sections[i]
    section_end = duration_sections[i + 1]
    
    # Filter homes within the current duration section
    filtered_duration = df[(df["No_rescue2"] >= section_start) & (df["No_rescue2"] < section_end)]
    
    # Calculate the angle of each home with respect to the center of the town for the current duration section
    angles = np.arctan2(filtered_duration["Relative_Y"], filtered_duration["Relative_X"])
    angles_deg = np.degrees(angles)
    angles_deg = (angles_deg+360) %360 
    
    # Calculate the histogram for the current duration section
    hist, bin_edges = np.histogram(np.radians(angles_deg), bins=num_bins, range=(0, 2 * np.pi))
    
    # Normalize the histogram bars to percentage within each direction
    total_homes_in_direction = len(filtered_duration)
    #hist_percentage = (hist / total_homes_in_direction) * 100
    hist_percentage=hist
    print(hist_percentage)
    
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    ax.bar(bin_centers, hist_percentage, width=(2 * np.pi / num_bins), alpha=0.7, edgecolor='k', linewidth=1, color=colors[i],
           label=f"{section_start}-{section_end} hours", bottom=bottom)
    
    
    bottom += hist_percentage
print(bottom)


# Set the number of ticks and corresponding tick labels for the compass directions
compass_directions = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
num_ticks = len(compass_directions)
ax.set_xticks(np.linspace(0, 2 * np.pi, num_ticks, endpoint=False))
ax.set_xticklabels(compass_directions)
ax.grid(linestyle='dashed')

ax.legend(loc='upper right')
plt.savefig("polar_rose_diagram_RescueInterruption.png", dpi=300)
plt.grid(True)
plt.show()







