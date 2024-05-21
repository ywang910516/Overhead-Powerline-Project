import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Load the data
data = pd.read_excel('../Data/evacuation-resuce-timeseries-data.xlsx')

data['time'] = pd.to_datetime(data['time'])
data_increase_rate = data.copy()
data_increase_rate['non-evacuable increase'] = data['non-evacuable number'].pct_change()
data_increase_rate['unrescuable increase'] = data['unrescuable number'].pct_change()

# Calculate the specific times when the number of non-evacuable and non-rescuable buildings increases significantly
# Here we are using the 95th percentile as the threshold for "significant increase"
threshold_non_evacuable = data_increase_rate['non-evacuable increase'].quantile(0.95)
threshold_unrescuable = data_increase_rate['unrescuable increase'].quantile(0.95)

significant_increase_times_non_evacuable = data_increase_rate['time'][data_increase_rate['non-evacuable increase'] > threshold_non_evacuable]
significant_increase_times_unrescuable = data_increase_rate['time'][data_increase_rate['unrescuable increase'] > threshold_unrescuable]

plt.figure(figsize=(15, 5))
bar_positions = np.arange(len(data['time']))
width = 0.3       

plt.bar(bar_positions-width/2, data['non-evacuable number'], width, label='Non-evacuable buildings', alpha=0.7)
plt.bar(bar_positions+width/2, data['unrescuable number'], width, label='Non-rescuable buildings', alpha=0.7)

for i in range(len(bar_positions)):
    plt.text(i-width/2, data['non-evacuable number'].iloc[i] + 0.5, str(data['non-evacuable number'].iloc[i]), ha = 'center')
    plt.text(i+width/2, data['unrescuable number'].iloc[i] + 0.5, str(data['unrescuable number'].iloc[i]), ha = 'center')

plt.xlabel('Date and Time')
plt.ylabel('Number of Buildings')
plt.title('Number of Non-evacuable and Non-rescuable Buildings Over Time')
time_labels = data['time'].dt.strftime('%m-%d %H:00')
plt.xticks(ticks=bar_positions, labels=time_labels, rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("../plot/no-evac-no-resc-TS.png", dpi=300)
plt.show()

# Printing the rate of increase
print("Rate of increase for non-evacuable buildings:")
print(data_increase_rate['non-evacuable increase'].describe())
print("\nRate of increase for non-rescuable buildings:")
print(data_increase_rate['unrescuable increase'].describe())

print("\nSpecific times when the number of non-evacuable buildings increases significantly:")
print(significant_increase_times_non_evacuable)
print("\nSpecific times when the number of non-rescuable buildings increases significantly:")
print(significant_increase_times_unrescuable)
