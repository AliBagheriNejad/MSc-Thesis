import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import os
from scipy import signal


# Changing working directory
os.chdir(r'G:\Masters\Thesis\Data\data')

# Get all files in the directory
current_path = os.getcwd()
file_names = os.listdir(current_path)

# Get .csv files
csv_files = []
for file in file_names:

    if '.csv' in file:
        csv_files.append(file)

# Reading files
dfs =[]
for file in csv_files:

    df = pd.read_csv(file)
    dfs.append(df)

# Combine all dataframes
test_df = pd.concat(dfs, axis=0, ignore_index=True)

# Extracting all data
all_data = np.zeros((test_df.shape[0],25000))

for i, data in enumerate(test_df.data):

    data = eval(data)
    data = np.array(data).reshape(-1,)
    data = signal.detrend(data) # Detrending the signal
    all_data[i,:] = data

# Create figure and axes
fig, ax = plt.subplots()

# Set up the lines
comp_line, = ax.plot([], [], 'b', lw=2, label='COMP')
turb_line, = ax.plot([], [], 'r', lw=2, label='TURB')

# Set up labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()

# Define initialization function
def init():
    comp_line.set_data([], [])
    turb_line.set_data([], [])
    return comp_line, turb_line

# Define update function
def update(i):
    # Update data for COMP line
    xx = all_data[2][0:i]
    yy = all_data[5][0:i]
    comp_line.set_data(xx, yy)
    
    # Update data for TURB line
    xx = all_data[18][0:i]
    yy = all_data[21][0:i]
    turb_line.set_data(xx, yy)
    
    return comp_line, turb_line
#%%
# Create animation
ani = animation.FuncAnimation(fig, update, frames=range(1, 1000),
                              init_func=init, blit=True, interval=2)


plt.xlim([-0.15,0.15])
plt.ylim([-0.15,0.15])
plt.grid('major')
# Show the animation
plt.show()
# %%
