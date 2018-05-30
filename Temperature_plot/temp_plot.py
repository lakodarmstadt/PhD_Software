import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Read the files:
roomtemp_filename = '/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/Messungen/Temperaturstabilitaet_SLS_Cavity/Temp_log_2018_05_25/sensorData_2018-05-25 07_23_00_2018-05-29 16_33_00.csv'
thermistor_filename = '/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/Messungen/Temperaturstabilitaet_SLS_Cavity/Temp_log_2018_05_25/Temp_log_2018_05_25_to_2018_05_29.txt'

roomtemp_df = pd.read_csv(roomtemp_filename, skiprows=10, skip_blank_lines=True)
thermistor_df = pd.read_csv(thermistor_filename, skiprows=10, skip_blank_lines=True, names=['date', 'resistance'])

# print(roomtemp_df)
# print(thermistor_df)

min_date, max_date = thermistor_df['date'].min(), thermistor_df['date'].max()
print(min_date, max_date)

print(roomtemp_df['date'].min() >= min_date)
print(roomtemp_df['date'].max() <= max_date)

# table2_temp_df = roomtemp_df[roomtemp_df.sensor_id == 39 & roomtemp_df.date >= min_date & roomtemp_df.date <= max_date]
table2_temp_df = roomtemp_df[(roomtemp_df['sensor_id'] == 39) & (roomtemp_df['date'] >= min_date) & (roomtemp_df['date'] <= max_date)]


table2_temp_df['date'] = pd.to_datetime(table2_temp_df['date'], format='%Y-%m-%d %H:%M:%S')
thermistor_df['date'] = pd.to_datetime(thermistor_df['date'], format='%Y-%m-%d %H:%M:%S.%f')

# print(table2_temp_df)
print(thermistor_df['date'])


fig, ax1 = plt.subplots(figsize=(50, 5))

ax1.plot(thermistor_df['date'], thermistor_df['resistance'], 'b.')
ax1.set_xlabel('date [UTC]')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Resistance thermistor', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(table2_temp_df['date'], table2_temp_df['value'], 'r.')
ax2.set_ylabel('temperature_table', color='r')
ax2.tick_params('y', colors='r')

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%y %m %d'))


# rotate and align the tick labels so they look better
fig.autofmt_xdate()


# ax1.xaxis_date()

# days = mdates.DayLocator(interval=1)
# hours = mdates.HourLocator()

# ax1.xaxis.set_major_locator(days)
# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%y %m %d'))


# fig.tight_layout()
# plt.show()
plt.savefig('/home/lars/Dokumente/Lars_Kohfahl/Studium/PhD/Messungen/Temperaturstabilitaet_SLS_Cavity/Temp_log_2018_05_25/temp_plot.png')

# plt.plot(table2_temp_df['date'], table2_temp_df['value'])
# plt.plot(thermistor_df['date'], thermistor_df['resistance'])
# plt.show()
