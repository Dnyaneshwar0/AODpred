from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

file = Dataset('test/data/MOD021/MOD021_01.hdf', 'r')

# Print all the variable keys to inspect available datasets
print("Available variables:")
print(file.variables.keys())

# Retrieve and print the long and latitude data
# long = file.variables['Longitude'][:]
# lat = file.variables['Latitude'][:]

b1=file.variables['EV_250_Aggr1km_RefSB'][0]
b3=file.variables['EV_500_Aggr1km_RefSB'][0]
b4=file.variables['EV_500_Aggr1km_RefSB'][1]
b7=file.variables['EV_500_Aggr1km_RefSB'][4]
b32=file.variables['EV_1KM_Emissive'][11]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.subplots_adjust(hspace=0.4, wspace=0.3) 

# Plot each dataset using plt.scatter() on the respective subplot
datasets = [b1, b3, b4, b7, b32]
titles = ["b1", "b3", "b4", "b7", "b32"]

x, y = np.meshgrid(range(datasets[0].shape[1]), range(datasets[0].shape[0]))
x_coords = x.flatten()
y_coords = y.flatten()

for i, ax in enumerate(axes.flatten()[:len(datasets)]):
    values = datasets[i].flatten()

    # Scatter plot for the current dataset
    ax.scatter(x_coords, y_coords, c=values, cmap='viridis', s=10)
    ax.set_title(f"Scatter Plot {titles[i]}")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

# Turn off any unused subplot (if there are extra slots in the grid)
for ax in axes.flatten()[len(datasets):]:
    ax.axis('off')
    
# Show the plots
plt.show()

