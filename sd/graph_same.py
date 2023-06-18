import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.signal import medfilt
from matplotlib.lines import Line2D

# List of CSV filenames
filename = '02-03.csv'
filenames = [filename]  # Add more filenames if needed
title = 'Air Quality Parameters'

# Read the CSV file
df = pd.read_csv(filenames[0])
# Extract the relevant columns
time_diff = df['UTC Time']
co2_ppm = df['CO2 ppm']
so2_ppm = df['SO2 ppm']
temperature = df['Temperature °']
humidity = df['Relative Humidity']
pm25_ppm = df['MC2.5 #/cm^3']
# Define the function to remove spikes
def remove_spikes(data, threshold=2):
    
    return data

# Apply spike removal to the variables
co2_ppm_filtered = remove_spikes(co2_ppm)
so2_ppm_filtered = remove_spikes(so2_ppm)
temperature_filtered = remove_spikes(temperature)
humidity_filtered = remove_spikes(humidity)
pm25_ppm_filtered = remove_spikes(pm25_ppm)

"""

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
"""
# Divide the data into three segments
segment_length = len(co2_ppm) // 3

segment1 = np.arange(segment_length)
segment2 = np.arange(segment_length, 2 * segment_length)
segment3 = np.arange(2 * segment_length, len(co2_ppm))
segments = [
        segment1,
        segment2,
        segment3
]

variables = [
    temperature_filtered,
    humidity_filtered,
    co2_ppm_filtered,
    pm25_ppm_filtered,
]

labels = [
    'Temperature (°C)',
    'Relative Humidity (%)',
    'CO2 (ppm)',
    'PM2.5 (#/cm^3)',
]
segment_colors = ['blue', 'green', 'orange']  # Colors for each segment
segment_labels = ['UAV OFF, Enclosed', 'UAV ON, Enclosed', 'UAV ON, Not Enclosed']  # Custom segment labels

# Plot all variables in a single figure with multiple subplots and overlapping segments
fig, axes = plt.subplots(len(variables), 1, figsize=(10, 15), sharex=True)


title = 'Experiment 2: Test %d' % (int(filename[4]))
fig.suptitle(title, fontsize=16)

# Iterate over each variable and its corresponding label
for ax, variable, label in zip(axes, variables, labels):
    # Plot each segment of the variable with a label for the legend
    handles = []  # List to store the legend handles
    for i, segment in enumerate(segments):
        segment_label = segment_labels[i]
        line = ax.plot(np.multiply(segment, 3.5), variable[segment], color=segment_colors[i], label=segment_label)
        handles.append(line[0])

        # Calculate the median of the current segment for the variable
        segment_median = np.percentile(variable[segment], 30)

        # Plot the median line starting from the beginning of the segment and ending at the end of the segment
        median_line = ax.axhline(y=segment_median, color=segment_colors[i], linestyle='--',
                                 xmin=segment[0] / len(co2_ppm), xmax=segment[-1] / len(co2_ppm))

        # Calculate the x-coordinate for the annotation
        x_coord = (3.5*segment[0] + 3.5*segment[-1]) / 2

        # Annotate the median value near the median line
        ax.annotate(f'{segment_median:.2f}', xy=(x_coord, segment_median),
                    xytext=(0, 10), textcoords='offset points', ha='center', color=segment_colors[i])

    # Add a legend entry with a broken line
    broken_line = Line2D([], [], linestyle='--', color='black', label='30th Percentile')
    handles.append(broken_line)

    ax.set_ylabel(label)

# Add a common legend for all subplots
fig.legend(handles, [handle.get_label() for handle in handles], loc='upper left', fontsize='small')

axes[-1].set_xlabel('Data Points')
plt.tight_layout()
fig.subplots_adjust(top=0.92)  # Adjust the spacing between suptitle and subplots
plt.show()
