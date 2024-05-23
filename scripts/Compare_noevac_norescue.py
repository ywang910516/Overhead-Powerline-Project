##########################################################################################################
#Python Script for post processing of Network analysis:
##########################################################################################################



########################################################################
#Generate plot that compare non-rescuable houses and non-evacuable houses
########################################################################


import pandas as pd
import matplotlib.pyplot as plt
import re

missing_counts_evac = pd.read_csv("../Data/missing_counts_evac_early.csv")
missing_counts_rescue = pd.read_csv("../Data/missing_counts_rescue.csv")

timestamp = missing_counts_rescue['filename'].apply(lambda x: re.search(r'(\d{4}_\d{2})', x).group(1) if re.search(r'(\d{4}_\d{2})', x) else None)

missing_counts_evac_column = missing_counts_evac.iloc[:, 1]
missing_counts_rescue_column = missing_counts_rescue.iloc[:, 1]

comparison = pd.DataFrame()
comparison['timestamp'] = timestamp
comparison['missing_counts_evac'] = missing_counts_evac_column
comparison['missing_counts_rescue'] = missing_counts_rescue_column

# Barchart parameter
bar_width = 0.35
opacity = 0.8
plt.figure(figsize=(15,10))

rects1 = plt.bar(comparison.index - bar_width/2, comparison['missing_counts_evac'], bar_width, alpha=opacity, color='b', label='non evac houses')
rects2 = plt.bar(comparison.index + bar_width/2, comparison['missing_counts_rescue'], bar_width, alpha=opacity, color='r', label='non rescue houses')

plt.xlabel('Timestamp')
plt.ylabel('Counts')
plt.title('Comparison of non-rescuable houses and non-evacuable houses')
plt.xticks(comparison.index, comparison['timestamp'], rotation=45) # Rotate x-axis labels for better readability

# Add value at the top of each bar
for rect in rects1 + rects2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2., 1.01*height, '%d' % int(height), ha='center', va='bottom')

plt.legend()
plt.tight_layout() # Adjust subplot parameters to give specified padding
plt.show()





