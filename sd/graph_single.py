import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def plot_segmented_percentile(csv_file, column_name, segment_start_index, percentile, y_label, offset):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)

    # Get the values of the specified column
    column_values = data[column_name].values

    # Split the column into two segments based on the segment_start_index
    lower_segment = column_values[:segment_start_index]
    upper_segment = column_values[segment_start_index:]

    # Calculate the percentile for each segment
    lower_percentile = np.percentile(lower_segment, percentile)
    upper_percentile = np.percentile(upper_segment, percentile)

    # Set colors for the segments and percentile lines
    lower_color = 'blue'
    upper_color = 'green'

    # Plot the lower segment and percentile line with thicker lines and different line styles
    plt.plot(np.arange(len(lower_segment)) * 3.5, lower_segment, color=lower_color, linestyle='-', linewidth=1.5, label='Enclosed')
    plt.plot([0, (segment_start_index - 1) * 3.5], [lower_percentile, lower_percentile], color=lower_color, linestyle='--', linewidth=1.5)
    plt.text((segment_start_index - 1) * 3.5 / 2, lower_percentile, f'{lower_percentile:.2f}', ha='center', va='bottom')

    # Plot the upper segment and percentile line with thicker lines and different line styles
    plt.plot(np.arange(segment_start_index, len(column_values)) * 3.5, upper_segment, color=upper_color, linestyle='-.', linewidth=1.5, label='Not Enclosed')
    plt.plot([(segment_start_index - 1) * 3.5, (len(column_values) - 1) * 3.5], [upper_percentile, upper_percentile], color=upper_color, linestyle='--', linewidth=1.5)
    plt.text(segment_start_index * 3.5 + (len(column_values) - segment_start_index) * 3.5 / 2, upper_percentile, f'{upper_percentile:.2f}', ha='center', va='bottom')
        # Set labels and title
    plt.xlabel('Time (s)')
    plt.ylabel(y_label)
    plt.title(column_name)

    # Clean up the x-axis labels to display integer values without decimals
    x_ticks = np.arange(0, len(column_values) * 3.5, 10)
    plt.xticks(x_ticks, [int(x_tick) for x_tick in x_ticks])

    # Set the y-axis limits to offset 
    plt.ylim(np.min(column_values) - offset, np.max(column_values) + offset)

    # Create legend entries for the segments
    enclosed_label = mlines.Line2D([], [], color=lower_color, linestyle='-',
                                   label='Enclosed')
    not_enclosed_label = mlines.Line2D([], [], color=upper_color, linestyle='-.',
                                       label='Not Enclosed')

    # Create a single legend entry for the percentile line
    percentile_line = mlines.Line2D([], [], color='gray', linestyle='--',
                                    label='{}th percentile'.format(percentile))
    percentile_line.set_dashes([2, 2])  # Set the dashes for the line

    # Display the legend with the entries
    plt.legend(handles=[enclosed_label, not_enclosed_label, percentile_line])

    # Display the plot
    plt.show()

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 7:
    print('Usage: python script.py <filename> <column_name> <segment_start_index> <percentile> <y_label>')
    sys.exit(1)

# Extract the command-line arguments
csv_file_path = sys.argv[1]
column_name_to_plot = sys.argv[2]
segment_start_index = int(sys.argv[3])
percentile_to_plot = float(sys.argv[4])
y_label = sys.argv[5]
offset = int(sys.argv[6])

# Call the plotting function with the provided arguments
plot_segmented_percentile(csv_file_path, column_name_to_plot, segment_start_index, percentile_to_plot, y_label, offset)
