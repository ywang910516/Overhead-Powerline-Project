##########################################################################################################
#Python Script for post processing of Network analysis:
##########################################################################################################



#####################################################################
#Compare the rescuable house at different time step with the main file and 
#get houses not rescuable at different time step
#####################################################################

import pandas as pd
import os

master_file = "../Data/ManvilleBldg1ftPlus_attribute.csv"

df_master = pd.read_csv(master_file)
master_ids = set(df_master['Id'])
csv_dir = '../Data/route_all_10ft'

# count missing properties that can be accessed by boat
# of each timestep during flood compare with the entire list of properties
missing_counts = []


for filename in os.listdir(csv_dir):
    if filename.endswith(".csv") and filename != master_file:
        df = pd.read_csv(os.path.join(csv_dir, filename))

        if 'IncidentID' not in df.columns:
            print(f'Skipping file {filename} as it does not contain an "IncidentID" column')
            continue
            
        file_ids = set(df['IncidentID'])
        
        missing_ids = master_ids - file_ids

        # Check if there are missing_ids, if yes, input it into a new list
        if len(missing_ids) > 0:
            df_missing = pd.DataFrame(list(missing_ids), columns=['Missing IncidentID'])
            output_filename = filename.split('.')[0] + '_rescue_missing.csv'
            df_missing.to_csv(output_filename, index=False)
            print(f'Written missing IncidentIDs to {output_filename}')

            missing_counts.append({
                'filename': output_filename,
                'missing_objects': len(missing_ids)
            })

        else:
            print(f'No missing IncidentIDs in {filename}')

df_counts = pd.DataFrame(missing_counts)
df_counts.to_csv('missing_counts_rescue_missing.csv', index=False)

print("Process completed.")






