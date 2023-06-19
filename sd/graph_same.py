
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Function definitions

def read_csv(filename):
    df = pd.read_csv(filename)
    return df

def remove_spikes(data, threshold=2):
    # Spike removal logic
    return data

def divide_segments(data_length, num_segments):
    segment_length = data_length // num_segments
    remaining_length = data_length % num_segments

    segments = []
    start_index = 0

    for i in range(num_segments):
        end_index = start_index + segment_length

        # Distribute the remaining data points evenly among the segments
        if remaining_length > 0:
            end_index += 1
            remaining_length -= 1

        segment = np.arange(start_index, end_index)
        segments.append(segment)
        start_index = end_index

    return segments

def plot_segments(axes, segments, variables, labels, segment_labels, segment_colors):
    handles = []
    for ax, variable, label in zip(axes, variables, labels):
        for i, segment in enumerate(segments):
            segment_label = segment_labels[i]
            line = ax.plot(segment*3.5, variable[segment], color=segment_colors[i], label=segment_label)
            handles.append(line[0])

            segment_median = np.percentile(variable[segment], 25)
            median_line = ax.axhline(y=segment_median, color=segment_colors[i], linestyle='--',
                                     xmin=segment[0] / len(variable), xmax=segment[-1] / len(variable))

            x_coord = np.mean(segment*3.5)
            ax.annotate(f'{segment_median:.2f}', xy=(x_coord, segment_median),
                        xytext=(0, 10), textcoords='offset points', ha='center', color=segment_colors[i])

        broken_line = Line2D([], [], linestyle='--', color='black', label='25th Percentile')
        handles.append(broken_line)

        ax.set_ylabel(label)

    return handles


def main(filename, second_segment_start=0, third_segment_start=0):
    # Read the CSV file
    df = read_csv(filename)

    # Extract the relevant columns
    co2_ppm = df['CO2 ppm']
    humidity = df['Relative Humidity']
    temperature = df['Temperature °']
    pm25_ppm = df['MC2.5 #/cm^3']

    # Apply spike removal to the variables
    co2_ppm_filtered = remove_spikes(co2_ppm)
    humidity_filtered = remove_spikes(humidity)
    temperature_filtered = remove_spikes(temperature)
    pm25_ppm_filtered = remove_spikes(pm25_ppm)

    variables = [temperature_filtered, humidity_filtered, co2_ppm_filtered, pm25_ppm_filtered]
    labels = ['Temperature (°C)', 'Relative Humidity (%)', 'CO2 (ppm)', 'PM2.5 (#/cm^3)']
    segment_colors = ['blue', 'green', 'orange']
    segment_labels = ['UAV OFF, Enclosed', 'UAV ON, Enclosed', 'UAV ON, Not Enclosed']

    num_segments = 3

    # Define the start indices of the segments based on the inputs or default values
    segments = []
    segments.append(np.arange(0, second_segment_start))
    segments.append(np.arange(second_segment_start, third_segment_start))
    segments.append(np.arange(third_segment_start, len(co2_ppm)))

    # Plot all variables in a single figure with multiple subplots and overlapping segments
    fig, axes = plt.subplots(len(variables), 1, figsize=(10, 15), sharex=True)
    title = 'Experiment 2: Test ' + filename[4:6]
    fig.suptitle(title, fontsize=16)

    handles = plot_segments(axes, segments, variables, labels, segment_labels, segment_colors)
    handles = handles[:4]
    fig.legend(handles, [handle.get_label() for handle in handles], loc='upper left', fontsize='small')
    fig.text(0.5, 0.02, 'time (s)', ha='center')
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    plt.show()

if __name__ == "__main__":
    # Retrieve the filename and start indices of the second and third segments from the command line arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        second_segment_start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        third_segment_start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        main(filename, second_segment_start, third_segment_start)
    else:
        print("Please provide a filename as a command line argument.")
        sys.exit(1)
