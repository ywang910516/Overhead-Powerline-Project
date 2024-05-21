import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv('../Data/height_difference_v2.csv')
data.head()

data['Ht_Diff']=data['Ht_Diff']/3.28084 #convert unit from feet to meter
# Calculate the 5th and 95th percentiles
p5 = np.percentile(data['Ht_Diff'], 5)
p95 = np.percentile(data['Ht_Diff'], 95)
p50 = np.percentile(data['Ht_Diff'],50)
print(p50)

height_diff_arr = data['Ht_Diff'].values
weights = np.ones_like(height_diff_arr) / len(height_diff_arr)

plt.figure(figsize=(10, 3))
plt.hist(height_diff_arr, bins=30, alpha=0.5, color='g', edgecolor='black',weights=weights)
plt.axvline(x=p5, color='r', linestyle='--', label=f'5th percentile ({p5:.2f} m)')
plt.axvline(x=p95, color='b', linestyle='--', label=f'95th percentile ({p95:.2f} m)')
plt.title('Histogram of Powerline Height')
plt.xlabel('Height (meters)')
plt.ylabel('Frequency')
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("../plot/Powerline_hist.png", dpi=300)

plt.show()
