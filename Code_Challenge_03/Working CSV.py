import csv
from collections import defaultdict

# Define the path to the CSV file
csv_file = "your_dataset.csv"

# Create a defaultdict to store the daily values for each year
yearly_data = defaultdict(list)
all_values = []  # List to store all daily values

# Read the CSV file and store the data by year
with open('C:\\GitHub\\NRS_528\\Code Challenge 03\\co-ppm-daily.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        date, value = row
        all_values.append(float(value))  # Append value to the list of all values
        year = date.split('/')[2]
        yearly_data[year].append((date, float(value)))

# Calculate the annual average for each year
annual_averages = {}
for year, values in yearly_data.items():
    annual_averages[year] = sum(val[1] for val in values) / len(values)

# Calculate the maximum, minimum, and average for the entire dataset
overall_min = min(all_values)
overall_max = max(all_values)
overall_avg = sum(all_values) / len(all_values)

# Calculate seasonal averages
seasonal_averages = defaultdict(float)
season_counts = defaultdict(int)
for year, values in yearly_data.items():
    for date, value in values:
        month = int(date.split('/')[0])
        if month in [3, 4, 5]:
            seasonal_averages['Spring'] += value
            season_counts['Spring'] += 1
        elif month in [6, 7, 8]:
            seasonal_averages['Summer'] += value
            season_counts['Summer'] += 1
        elif month in [9, 10, 11]:
            seasonal_averages['Autumn'] += value
            season_counts['Autumn'] += 1
        elif month in [12, 1, 2]:
            seasonal_averages['Winter'] += value
            season_counts['Winter'] += 1

for season in seasonal_averages:
    seasonal_averages[season] /= season_counts[season]

# Calculate anomaly for each value in the dataset relative to the mean for the entire time series
anomalies = [(date, value - overall_avg) for year_value in yearly_data.values () for data, value in year_value]

# Print or do whatever you want with the results
print("Annual Averages:")
for year, avg in annual_averages.items():
    print("Year {}: Annual Average = {}".format(year, avg))

print("\nOverall Statistics:")
print("Minimum Value:", overall_min)
print("Maximum Value:", overall_max)
print("Overall Average:", overall_avg)

print("\nSeasonal Averages:")
for season, avg in seasonal_averages.items():
    print("{}: {}".format(season, avg))
#
print("\nAnomalies Relative to Overall Mean:")
print(anomalies)  # Debug print
for date, anomaly in anomalies:
    print("{}: {}".format(anomaly[20], anomaly[30]))
