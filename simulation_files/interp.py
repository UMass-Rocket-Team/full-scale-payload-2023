import pandas as pd
import numpy as np

# read in the CSV file
df = pd.read_csv(r'/Users/demetriliousas/Downloads/new_data.csv')

# create a new time column with the desired timestep of 0.001s
new_time = np.arange(df['Time'].iloc[0], df['Time'].iloc[-1], 0.001)
df_new = pd.DataFrame({'Time': new_time})

# loop over each column in the original dataframe (excluding the "Time" column)
for col in df.columns[1:]:
    
    # create a linear interpolation function for the column
    f = np.interp(new_time, df['Time'], df[col])
    
    # add the interpolated column to the new dataframe
    df_new[col] = f

# write the new dataframe to a CSV file
df_new.to_csv(r'/Users/demetriliousas/Downloads/interp_data.csv', index=False)
