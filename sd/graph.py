import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# List of CSV filenames
filenames = ['mark.csv']  # Add more filenames if needed
title = 'Air Quality Parameters'

# Create subplots for each parameter
num_params = 8  # Number of parameters to plot
num_files = len(filenames)
num_rows = (num_params + 1) // 2  # Adjust the number of rows based on the number of parameters
fig, axs = plt.subplots(num_rows, 2, figsize=(12, num_rows * 4))
fig.suptitle(title)

# Iterate over the CSV files and plot the data
for i, filename in enumerate(filenames):
    # Read the CSV file
    df = pd.read_csv(filename)
    # Extract the relevant columns
    utc_time = df['UTC Time']
    co2_ppm = df['CO2 ppm']
    so2_ppm = df['SO2 ppm']
    temperature = df['Temperature °']
    humidity = df['Relative Humidity']
    pm25_ppm = df['PM2.5 ppm']
    pm10_ppm = df['PM10 ppm']
    nc25 = df['NC2.5 #/cm^3']
    nc10 = df['NC10 #/cm^3']

    z_scores = np.abs(stats.zscore(df['SO2 ppm']))
    threshold = 3
    outlier_mask = z_scores > threshold
    df_filtered = df.copy()
    df_filtered.loc[outlier_mask, 'SO2 ppm'] = np.nan
    so2_ppm = df_filtered['SO2 ppm']
    # Extract hours, minutes, and seconds from the first element
    hours1 = int(str(utc_time[0])[:2])
    minutes1 = int(str(utc_time[0])[2:4])
    seconds1 = int(str(utc_time[0])[4:6])

    # Calculate total seconds for the first time value
    total_seconds1 = hours1 * 3600 + minutes1 * 60 + seconds1

    # Initialize a list to store the time differences in seconds
    time_diff = []

    # Loop through the remaining elements and calculate time differences
    for i in range(0, len(utc_time)):
        current_time = utc_time[i]
        hours2 = int(str(current_time)[:2])
        minutes2 = int(str(current_time)[2:4])
        seconds2 = int(str(current_time)[4:6])

        # Calculate total seconds for the current time value
        total_seconds2 = hours2 * 3600 + minutes2 * 60 + seconds2


        # Calculate time difference in seconds and append to the list
        time_diff.append(total_seconds2 - (hours1 * 3600 + minutes1 * 60 + seconds1))
    # Plot Temperature
    axs[0, 0].plot(time_diff, temperature, marker='o', label=filename, markersize=1)
    axs[0, 0].set_xlabel('time (s)')
    axs[0, 0].set_ylabel('°C')
    axs[0, 0].set_title('Temperature')
    axs[0, 0].legend()

    # Plot Relative Humidity
    axs[0, 1].plot(time_diff, humidity, marker='o', label=filename, markersize=1)
    axs[0, 1].set_xlabel('time (s)')
    axs[0, 1].set_ylabel('%')
    axs[0, 1].set_title('Relative Humidity')
    axs[0, 1].legend()

    # Plot CO2 ppm
    axs[1, 0].plot(time_diff, co2_ppm, marker='o', label=filename, markersize=1)
    axs[1, 0].set_xlabel('time (s)')
    axs[1, 0].set_ylabel('ppm')
    axs[1, 0].set_title('CO2 concentration')
    axs[1, 0].legend()

    # Plot SO2 ppm
    axs[1, 1].plot(time_diff, so2_ppm, marker='o', label=filename, markersize=1)
    axs[1, 1].set_xlabel('time (s)')
    axs[1, 1].set_ylabel('ppm')
    axs[1, 1].set_title('SO2 Concentration')
    axs[1, 1].legend()

    # Plot PM2.5 ppm
    axs[2, 0].plot(time_diff, pm25_ppm, marker='o', label=filename, markersize=1)
    axs[2, 0].set_xlabel('time (s)')
    axs[2, 0].set_ylabel('ppm')
    axs[2, 0].set_title('PM2.5 Mass Concentration')
    axs[2, 0].legend()

    # Plot nc2.5 #/cm^3
    axs[2, 1].plot(time_diff, nc25, marker='o', label=filename, markersize=1)
    axs[2, 1].set_xlabel('time (s)')
    axs[2, 1].set_ylabel('#/cm^3')
    axs[2, 1].set_title('PM2.5 Number Concentration')
    axs[2, 1].legend()

    # Plot PM10 ppm
    axs[3, 0].plot(time_diff, pm10_ppm, marker='o', label=filename, markersize=1)
    axs[3, 0].set_xlabel('time (s)')
    axs[3, 0].set_ylabel('ppm')
    axs[3, 0].set_title('PM10 Mass Concentration')
    axs[3, 0].legend()

    # Plot nc10 #/cm^3
    axs[3, 1].plot(time_diff, nc10, marker='o', label=filename, markersize=1)
    axs[3, 1].set_xlabel('time (s)')
    axs[3, 1].set_ylabel('#/cm^3')
    axs[3, 1].set_title('PM10 Number Concentration')
    axs[3, 1].legend()

# Adjust subplot spacing
plt.subplots_adjust(hspace=0.8, wspace=0.3)

# Display the graph
plt.show()
