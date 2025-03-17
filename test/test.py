# Import necessary libraries
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Step 1: Open the HDF file and read datasets ===
# Replace 'your_file.hdf' with the path to your MODIS HDF file
file = Dataset('data.hdf', 'r')

# Load latitude, longitude, AOD, and quality flag datasets
latitude = file.variables['Latitude'][:]  # Latitude array
longitude = file.variables['Longitude'][:]  # Longitude array
aod = file.variables['Optical_Depth_Land_And_Ocean'][:]  # AOD data
quality_flag = file.variables['Land_Ocean_Quality_Flag'][:]  # Quality assurance flags

# === Step 2: Handle missing or invalid values ===
# Replace invalid AOD values (-9999) with NaN
aod = np.where(aod == -9999, np.nan, aod)

# Apply a mask using the quality flag (retain only valid data points)
# For this example, assume quality_flag > 0 indicates valid data
valid_mask = (quality_flag > 0)
aod = np.where(valid_mask, aod, np.nan)

# === Step 3: Flatten the data ===
# Flatten latitude, longitude, and AOD arrays for easier structuring
latitude = latitude.flatten()
longitude = longitude.flatten()
aod = aod.flatten()

# === Step 4: Organize data into a Pandas DataFrame ===
# Create a DataFrame for structured data processing
data = {
    'Latitude': latitude,
    'Longitude': longitude,
    'AOD': aod
}
df = pd.DataFrame(data)

# Remove rows with NaN values (invalid or missing data)
df.dropna(inplace=True)

# Print the first few rows of the cleaned DataFrame
print("Cleaned Data Preview:")
print(df.head())

# === Step 5: Save the cleaned data ===
# Save the cleaned DataFrame to a CSV file
df.to_csv('cleaned_aod_data.csv', index=False)
print("Cleaned data saved to 'cleaned_aod_data.csv'.")

# === Step 6: Visualize the data in subplots ===
# Create a single figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6))  # 1 row, 2 columns of subplots

# Scatter plot in the first subplot
scatter = axes[0].scatter(df['Longitude'], df['Latitude'], c=df['AOD'], cmap='viridis', s=1)
axes[0].set_title('Spatial Distribution of AOD')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')
fig.colorbar(scatter, ax=axes[0], label='AOD')  # Add a colorbar to the scatter plot

# Histogram in the second subplot
axes[1].hist(df['AOD'], bins=50, color='blue', edgecolor='black')
axes[1].set_title('AOD Value Distribution')
axes[1].set_xlabel('AOD')
axes[1].set_ylabel('Frequency')

# Adjust layout for readability
plt.tight_layout()

# Display the plots
plt.show()
