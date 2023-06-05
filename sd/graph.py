
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from datetime import datetime
from dateutil import parser

# Read the CSV file
df = pd.read_csv('data.csv')

# Extract the relevant columns
utc_time = df['UTC Time']
co2_ppm = df['CO2 ppm']
so2_ppm = df['SO2 ppm']
temperature = df['Temperature °']
humidity = df['Relative Humidity %']
pm25_ppm = df['PM2.5 ppm']
pm10_ppm = df['PM10 ppm']
nc25 = df['NC2.5 #/cm^3']
nc10 = df['NC10 #/cm^3']

# Convert UTC time to local time zone (Asia/Manila)
local_timezone = pytz.timezone('Asia/Manila')
local_time = [parser.parse(str(t)).replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone("Asia/Manila")).strftime("%H:%M:%S") for t in utc_time]

# Create subplots for each parameter
fig, axs = plt.subplots(3, 2, figsize=(12, 10))
fig.suptitle('Air Quality Parameters')

# Plot CO2 ppm
axs[0, 0].plot(local_time, co2_ppm, marker='o')
axs[0, 0].set_xlabel('PH Time')
axs[0, 0].set_ylabel('ppm')
axs[0, 0].set_title('CO2 concentration')

# Plot SO2 ppm
axs[0, 1].plot(local_time, so2_ppm, marker='o')
axs[0, 1].set_xlabel('PH Time')
axs[0, 1].set_ylabel('ppm')
axs[0, 1].set_title('SO2 Concentration')

# Plot Temperature
axs[1, 0].plot(local_time, temperature, marker='o')
axs[1, 0].set_xlabel('PH Time')
axs[1, 0].set_ylabel('°C')
axs[1, 0].set_title('Temperature')

# Plot Relative Humidity
axs[1, 1].plot(local_time, humidity, marker='o')
axs[1, 1].set_xlabel('Local Time')
axs[1, 1].set_ylabel('%')
axs[1, 1].set_title('Relative Humidity')

# Plot PM2.5 ppm
axs[2, 0].plot(local_time, pm25_ppm, marker='o')
axs[2, 0].set_xlabel('Local Time')
axs[2, 0].set_ylabel('ppm')
axs[2, 0].set_title('PM2.5 Concentration')

# Plot PM10 ppm
axs[2, 1].plot(local_time, pm10_ppm, marker='o')
axs[2, 1].set_xlabel('Local Time')
axs[2, 1].set_ylabel('ppm')
axs[2, 1].set_title('PM10 Concentration')

# Adjust layout and spacing
plt.tight_layout()

# Display the graph
plt.show()
