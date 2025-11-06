# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:15:26 2025

@author: Alessandro Pavan
apavan@ogs.it
"""


# Imports necessary libraries for plotting, date handling, data manipulation, and coordinate projection.
import matplotlib.pyplot as plt
import matplotlib.dates as md
# import numpy as np # This library is imported but not used in the current script.
import pandas as pd
from pyproj import Proj, transform

# Define the input filename for the CSV data.
filename = 'SRVY0-ACQU14-10Hz.csv'

# Initialize empty lists to store data extracted from the CSV file.
datetime_list = [] # Stores date and time strings (DD/MM/YYYY HH:MM:SS.sss)
lat = []           # Stores raw Latitude values
lon = []           # Stores raw Longitude values
alt = []           # Stores Altitude values (only for non-empty records)
datetime_alt = []  # Stores date and time strings corresponding to altitude points
mag = []           # Stores Magnetic field values
gga = []           # Stores GGA quality indicator values
nsat = []          # Stores Number of satellites used (for GGA records)
lat_gga = []       # Stores GGA Latitude converted to decimal degrees
lon_gga = []       # This list is initialized but not used in the loop
# Note: The original code used 'dataora'/'dataora2' and 'latgga'/'longga' for these variables.

# Define the specific time string to search for within the dataset.
time_to_search = '9:44:20.000' 

# Read the CSV file, skipping the first line (header).
data = open(filename).readlines()[1:]

# Loop through each line of the data (starting from the second line of the file).
for line in data:
    # Split the line by comma to get individual fields (tokens).
    split_line = line.split(',')
    s = split_line # Shorthand for the split line list.

    # Append Date (s[1]) and Time (s[2]) concatenated as a single datetime string.
    datetime_list.append(s[1] + ' ' + s[2])
    # Append Latitude (s[3]) and Longitude (s[4]) as floats.
    lat.append(float(s[3]))
    lon.append(float(s[4]))

    # Check if the Altitude field (s[24]) is non-empty. This indicates valid GGA data is present.
    if s[24] != "":
        # Append Altitude, and the corresponding datetime string.
        alt.append(float(s[24]))
        datetime_alt.append(s[1] + ' ' + s[2])
        # Append Number of satellites (s[21]).
        nsat.append(s[21])
        
    # Append Magnetic field value (s[5]) as a float for all records.
    mag.append(float(s[5]))
    # Append the GGA field (s[28]) for quality indicator.
    gga.append(s[28])
    
# Convert the list of datetime strings into a Pandas DatetimeIndex for plotting on the x-axis.
df = pd.to_datetime(datetime_list)
df2 = pd.to_datetime(datetime_alt)

#*** SEARCH FOR A SPECIFIC TIME
# Function to find the index of the first occurrence of a specific time string.
def find_index_by_time(data_list, time_to_search):
    # Iterate through the list of full datetime strings with their index.
    for index, full_datetime in enumerate(data_list):
        # Extract the time portion (including milliseconds) from the full datetime string.
        # The time starts after the first space.
        extracted_time = full_datetime.split(' ')[1]

        # Compare the extracted time with the target time string.
        if extracted_time == time_to_search:
            # If a match is found, return the index.
            return index
    
    # If the loop finishes without finding a match, return -1.
    return -1

# Call the function to find the index of the specified time.
index_found = find_index_by_time(datetime_list, time_to_search)

# Print the result of the time search
if index_found != -1:
    print(f"Il primo elemento con orario '{time_to_search}' si trova all'indice: {index_found}")
else:
    print(f"Nessun elemento con orario '{time_to_search}' è stato trovato nella lista.")
#******

#*** PLOTTING MAG AND ALTITUDE
# Create a figure and primary axes (ax1) for the plot.
fig, ax1 = plt.subplots()
# Set the size of the plot figure.
fig.set_size_inches(18, 8)
# Set the title of the plot.
plt.title('Mag and Height values')

# Create a secondary y-axis (ax2) that shares the same x-axis (twinx).
ax2 = ax1.twinx()

# --- Final modifications for the left y-axis (Magnetic Value) ---
# Set the color and thickness of only the left spine.
ax1.spines['left'].set_color('green')
ax1.spines['left'].set_linewidth(3)
# Explicitly turn off the other spines to prevent overlaps or confusion.
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['right'].set_visible(False)
# Set the color of the ticks and labels for the left axis to match the plot color.
ax1.tick_params(axis='y', colors='green', labelcolor='green')
# ---

# Set the color and position of the secondary y-axis (Altitude).
ax2.spines['right'].set_color('blue')
ax2.spines['right'].set_linewidth(3)

# Set the color of the ticks and labels for the secondary axis.
ax2.tick_params('y', colors='b')

# ---
# For completeness, explicitly turn off the secondary left spine.
ax2.spines['left'].set_visible(False)
# ---

# Plot the Magnetic values on the primary axis (ax1) as green dots.
ax1.plot(df, mag, 'g.')
# Plot the Altitude values on the secondary axis (ax2) as a blue line.
ax2.plot(df2, alt, 'b-')

# Set the labels for the two y-axes.
ax1.set_ylabel('Mag value (nT)', fontsize=12, color='g')
ax2.set_ylabel('Altitude (m)', fontsize=12, color='b')

# Configure the x-axis (time axis).
# Set major tick locations to every minute.
ax1.xaxis.set_major_locator(md.MinuteLocator())
# Format the major tick labels to show Hour:Minute:Second.
ax1.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))

# Apply 90-degree rotation to the x-axis tick labels for better readability.
ax1.tick_params(axis='x', rotation=90)
# Adjust plot parameters for a tight layout.
plt.tight_layout()
# Add a vertical dashed line to mark the found time index, but only if an index was found.
if index_found != -1:
    ax1.axvline(x=df[index_found], color='k', linestyle='--', linewidth=2, label='punto')
# Display the plot.
plt.show()
# ******************

#****** COORDINATE TRANSFORMATION
# Define the input projection (datum='WGS84', projection='latlong' - standard Lat/Lon).
iproj = Proj(datum='WGS84',proj='latlong')

# Define the output projection (datum='WGS84', projection='utm', zone='33').
# This converts the coordinates to UTM Zone 33.
oproj = Proj(datum='WGS84',proj='utm', zone='33')

# Perform the coordinate transformation from the input projection (Lat/Lon)
# to the output projection (UTM Northing/Easting).
# The order of arguments is (input_proj, output_proj, longitude, latitude, radians=False).
x, y = transform(iproj, oproj, lon, lat, radians=False)


#****** PLOTTING TRAJECTORY
# Create a new figure and axes for the UTM trajectory plot.
fig, ax1 = plt.subplots()
fig.set_size_inches(10, 6)
# Set the plot title.
plt.title('Trajectory [UTM WGS84]')
# Plot the trajectory (Easting vs. Northing) as a cyan line.
ax1.plot(x, y, '-c')
# Mark the specific point found earlier with a black circle, but only if an index was found.
if index_found != -1:
    ax1.plot(x[index_found], y[index_found], 'ok')
# Set the x-axis label.
ax1.set_xlabel('Easting (m)')
# Set the y-axis label.
ax1.set_ylabel('Northing (m)')
# Set the color of the y-axis ticks to black.
ax1.tick_params('y', colors='k')
# Display the plot.
plt.show()
