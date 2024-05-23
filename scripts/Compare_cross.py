##########################################################################################################
#Python Script for post processing of Network analysis:
##########################################################################################################



####################################################
#Compare the evacuable house and rescuable house
#get house rescuable but non-evacuable, also get house
#evacuable but non-rescuable. 
#(Need a script to remove the "evac" in file name)
####################################################

import pandas as pd
import os

csv_dir_1 = "../Data/evac"
csv_dir_2 = "../Data/rescue"

for filename in os.listdir(csv_dir_1):

    if filename.endswith("evac.csv"):
        # determine the corresponding filename in the second directory
        filename_2 = filename.replace('evac', 'rescue')

        df1 = pd.read_csv(os.path.join(csv_dir_1, filename))
        df2 = pd.read_csv(os.path.join(csv_dir_2, filename_2))

        if 'IncidentID' not in df1.columns or 'IncidentID' not in df2.columns:
            print(f'Skipping file pair ({filename}, {filename_2}) as "ObjectID" column is missing in one or both files')
            continue

        set1 = set(df1['IncidentID'])
        set2 = set(df2['IncidentID'])

        # find properties in evacuable houses but not in rescuable houses
        difference1 = set1 - set2
        if difference1:
            df_diff1 = pd.DataFrame(list(difference1), columns=['In evac but not rescue'])
            output_filename1 = filename.split('.')[0] + '_in_evac_not_rescue.csv'
            df_diff1.to_csv(output_filename1, index=False)
            print(f'Written differences to {output_filename1}')

        # find find properties in rescuable houses but not in evacuable houses
        difference2 = set2 - set1
        if difference2:
            df_diff2 = pd.DataFrame(list(difference2), columns=['In rescue but not evac'])
            output_filename2 = filename.split('.')[0] + '_in_rescue_not_evac.csv'
            df_diff2.to_csv(output_filename2, index=False)
            print(f'Written differences to {output_filename2}')

        if not difference1 and not difference2:
            print(f'No differences between {filename} and {filename_2}')

print("Process completed.")

