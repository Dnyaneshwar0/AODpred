# Import necessary libraries
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Step 1: Open the HDF file and load datasets ===
# Replace 'data.hdf' with the path to your MODIS HDF file
file = Dataset('data_proc_bands.hdf', 'r')

# Load latitude, longitude, and SensorZenith datasets
latitude = file.variables['Latitude'][:]  # Latitude array
longitude = file.variables['Longitude'][:]  # Longitude array
sensor_zenith = file.variables['EV_250_Aggr1km_RefSB_Samples_Used'][:]  # Sensor zenith data

# === Step 2: Handle missing or invalid values ===
# Replace invalid SensorZenith values (e.g., -9999) with NaN
sensor_zenith = np.where(sensor_zenith == -9999, np.nan, sensor_zenith)

# Flatten latitude, longitude, and SensorZenith arrays for easier processing
latitude = latitude.flatten()
longitude = longitude.flatten()
sensor_zenith = sensor_zenith.flatten()

# Organize the data into a dictionary and convert to Pandas DataFrame
data = {
    'Latitude': latitude,
    'Longitude': longitude,
    'SensorZenith': sensor_zenith
}
df = pd.DataFrame(data)

# Remove rows with NaN values to clean the data
df.dropna(inplace=True)

# === Step 3: Visualize the data with a scatter plot ===
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['Longitude'], df['Latitude'], c=df['SensorZenith'], cmap='coolwarm', s=1)
plt.colorbar(scatter, label='Sensor Zenith Angle')
plt.title('Spatial Distribution of SensorZenith')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# === Step 4: Save the cleaned data (optional) ===
df.to_csv('cleaned_sensor_zenith_data.csv', index=False)
print("Cleaned data saved to 'cleaned_sensor_zenith_data.csv'.")
