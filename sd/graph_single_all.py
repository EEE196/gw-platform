import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def plot_segmented_percentile(csv_file, segment_start_index, percentile):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Define the columns to plot
    columns_to_plot = ['Temperature', 'Relative Humidity', 'CO2', 'PM2.5']

    # Set colors for the segments and percentile lines
    lower_color = 'blue'
    upper_color = 'green'

    # Create subplots for each variable
    num_plots = len(columns_to_plot)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, num_plots * 4), sharex=True)

    # Iterate over the columns to plot and corresponding axes
    for i, (column_name, ax) in enumerate(zip(columns_to_plot, axes)):
        # Get the values of the specified column
        column_values = data[column_name].values

        # Split the column into two segments based on the segment_start_index
        lower_segment = column_values[:segment_start_index]
        upper_segment = column_values[segment_start_index:]

        # Calculate the percentile for each segment
        lower_percentile = np.percentile(lower_segment, percentile)
        upper_percentile = np.percentile(upper_segment, percentile)

        # Plot the lower segment and percentile line with thicker lines and different line styles
        ax.plot(np.arange(len(lower_segment)) * 3.5, lower_segment, color=lower_color, linestyle='-', linewidth=1.5)
        ax.plot([0, (segment_start_index - 1) * 3.5], [lower_percentile, lower_percentile], color=lower_color, linestyle='--', linewidth=1.5)
        ax.text((segment_start_index - 1) * 3.5 / 2, lower_percentile, f'{lower_percentile:.2f}', ha='center', va='bottom')

        # Plot the upper segment and percentile line with thicker lines and different line styles
        ax.plot(np.arange(segment_start_index, len(column_values)) * 3.5, upper_segment, color=upper_color, linestyle='-.', linewidth=1.5)
        ax.plot([(segment_start_index - 1) * 3.5, (len(column_values) - 1) * 3.5], [upper_percentile, upper_percentile], color=upper_color, linestyle='--', linewidth=1.5)
        ax.text(segment_start_index * 3.5 + (len(column_values) - segment_start_index) * 3.5 / 2, upper_percentile, f'{upper_percentile:.2f}', ha='center', va='bottom')

        # Remove the subplot title
        ax.set_title('')

        # Set the ylabel as the column name with units
        units = ['°C', '%', 'ppm', 'ppm']
        ax.set_ylabel(f'{column_name} ({units[i]})')

        # Set the y-axis limits for each variable with a specified offset
        offset = 2
        min_value = np.min(column_values) - offset
        max_value = np.max(column_values) + offset
        ax.set_ylim(min_value, max_value)

    # Set the x-axis label
    plt.xlabel('Time (s)')
    # Create a single legend for all subplots
    enclosed_label = mlines.Line2D([], [], color=lower_color, linestyle='-',
                                   label='Enclosed')
    not_enclosed_label = mlines.Line2D([], [], color=upper_color, linestyle='-.',
                                       label='Not Enclosed')
    percentile_line = mlines.Line2D([], [], color='gray', linestyle='--',
                                    label='{}th percentile'.format(percentile))
    handles = [enclosed_label, not_enclosed_label, percentile_line]
    fig.legend(handles=handles, loc='upper left')

    # Set the figure title
    fig.suptitle(f'Without downwash vs With downwash: Test {csv_file[4]}')

    # Adjust the layout to prevent labels from being cut off
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Display the plot
    plt.show()

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 4:
    print('Usage: python script.py <filename> <segment_start_index> <percentile>')
    sys.exit(1)

# Extract the command-line arguments
csv_file_path = sys.argv[1]
segment_start_index = int(sys.argv[2])
percentile_to_plot = float(sys.argv[3])

# Call the plotting function with the provided arguments
plot_segmented_percentile(csv_file_path, segment_start_index, percentile_to_plot)
