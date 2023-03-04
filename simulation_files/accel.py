import pandas as pd
import numpy as np

# read in the CSV file
df = pd.read_csv(r'/Users/demetriliousas/Downloads/interp_data.csv')

# extract the magnitude column
mag_col = df['Acceleration']

# generate random values for the x, y, and z components
x = np.random.uniform(low=-1.0, high=1.0, size=len(mag_col))
y = np.random.uniform(low=-1.0, high=1.0, size=len(mag_col))
z = np.random.uniform(low=-1.0, high=1.0, size=len(mag_col))

# normalize the x, y, and z components so that their magnitudes sum to 1
norm = np.sqrt(np.sum(np.square([x, y, z]), axis=0))
x = x / norm
y = y / norm
z = z / norm

# calculate the magnitudes of the x, y, and z components
x_mag = x * mag_col
y_mag = y * mag_col
z_mag = z * mag_col

# calculate the total magnitude of the x, y, and z components
new_mag_col = np.sqrt(np.square(x_mag) + np.square(y_mag) + np.square(z_mag))

# normalize the x, y, and z components so that their magnitudes sum to the original total magnitude
x_mag = x_mag * (mag_col / new_mag_col)
y_mag = y_mag * (mag_col / new_mag_col)
z_mag = z_mag * (mag_col / new_mag_col)

# create new columns for the x, y, and z components
df['Acceleration_x'] = x_mag
df['Acceleration_y'] = y_mag
df['Acceleration_z'] = z_mag

# write the modified dataframe to a new CSV file
df.to_csv('/Users/demetriliousas/Downloads/sim_data.csv', index=False)