This Python program is designed to process, analyze, and visualize geospatial and magnetic field data extracted from a comma-separated values (CSV) file. The script performs data reading, specific record searching, time-series plotting of magnetic field and altitude, and coordinate transformation followed by trajectory plotting.

The program iterates through each line of the CSV file, extracting and storing fields into dedicated lists:
Time Series Data: Complete date and time strings (datetime_list), raw latitude (lat), raw longitude (lon), and magnetic field values (mag) are extracted for all records.
Altitude Data: Altitude (alt) and its corresponding datetime stamp (datetime_alt) are only extracted if the altitude field is non-empty, indicating valid GPS-GGA (Global Positioning System - Global Positioning data) information. The number of satellites (nsat) is also stored for these records.
Time Conversion: The collected datetime strings are converted into a pandas.DatetimeIndex (df and df2) for accurate time-series plotting.

A custom function, find_index_by_time, is defined to locate the index of the first data point matching a predefined time string (time_to_search = '9:44:20.000'). The script executes this search and prints the result, which is crucial for highlighting a specific event on the subsequent plots.

The script generates a single figure with two distinct Y-axes sharing a common X-axis (time):
Primary Axis (Left - Green): Plots the Magnetic field values (mag) over time.
Secondary Axis (Right - Blue): Plots the corresponding Altitude values (alt) over time, using only the records where altitude data was present.

If the search time was found, a vertical dashed line is added to mark the specific time-series index.

Using the pyproj library, the script converts the raw latitude and longitude coordinates from WGS84 Lat/Lon (datum='WGS84', to UTM Zone 33 (datum='WGS84', proj='utm', zone='33'). The transformed Easting and Northing coordinates are stored for trajectory plotting.

Finally, a separate figure is created to visualize the geospatial trajectory of the survey: The plot displays the Northing vs. Easting coordinates in the UTM projection. The trajectory is plotted as a continuous cyan line.If the time-based search was successful, the corresponding data point is explicitly marked with a black circle on the trajectory map.
