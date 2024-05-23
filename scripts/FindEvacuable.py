##########################################################################################################
#Python Script for post processing of Network analysis:
##########################################################################################################



#####################################################################
#Compare the evacable house at different time step with the main file
#and get houses not evacable at different time step
#####################################################################

import pandas as pd
import os

master_file = "D:/Work/powerline analysis/ManvilleBldg1ftPlus_attribute.csv"

df_master = pd.read_csv(master_file)
master_ids = set(df_master['Id'])
csv_dir = 'D:/Work/powerline analysis/evac_route_csv'

# count missing properties that can be accessed by walk or automobile
# of each timestep during flood compare with the entire list of properties
missing_counts = []


for filename in os.listdir(csv_dir):
    if filename.endswith(".csv") and filename != master_file:
        df = pd.read_csv(os.path.join(csv_dir, filename))

        if 'FacilityID' not in df.columns:
            print(f'Skipping file {filename} as it does not contain an "FacilityID" column')
            continue
            
        file_ids = set(df['FacilityID'])

        missing_ids = master_ids - file_ids

        # Check if there are missing_ids, if yes, input it into a new list
        if len(missing_ids) > 0:
            df_missing = pd.DataFrame(list(missing_ids), columns=['Missing ObjectID'])
            output_filename = filename.split('.')[0] + '_missing.csv'
            df_missing.to_csv(output_filename, index=False)
            print(f'Written missing ObjectIDs to {output_filename}')

            missing_counts.append({
                'filename': output_filename,
                'missing_objects': len(missing_ids)
            })

        else:
            print(f'No missing ObjectIDs in {filename}')

df_counts = pd.DataFrame(missing_counts)
df_counts.to_csv('missing_counts_evac.csv', index=False)

print("Process completed.")





