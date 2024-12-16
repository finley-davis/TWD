import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ruptures as rpt

#year range, this is can be changed based on what years you want to look at
start_year = 2000
end_year = 2020

#load in csv file
file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
#read file path to data variable
data = pd.read_csv(file_path)

#rename columns based on csv file, may have to change based on csv file (This needs to be revised in the future)
data.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16', 'Unnnamed17', 'Unnamed18']

#convert date column to datetime object
data['Date'] = pd.to_datetime(data['Date'], format='%Y', errors='coerce')

#drops rows with no date or depth (just a reassurance that there are no errors in the pre-filtered data)
data = data.dropna(subset=['Date', 'Depth'])
#converts date to year (just want 4 digits)
data['Year'] = data['Date'].dt.year
#filters data to only include years between start_year and end_year that was defined at the top
data = data[(data['Date'].dt.year >= start_year) & (data['Date'].dt.year <= end_year)]

#sorts data by year, .values is used to access numpy array (could also use .to_numpy())
signal = data['Depth'].values
model = "l2"  #cost function, chose 'l2' for depth trends

#detect change points using the Pelt algorithm
#can replace pelt with Binseg
#10 or less change points
algo = rpt.Pelt(model=model).fit(signal)
breakpoints = algo.predict(pen=50)  

#plot results with change points marked
plt.figure(figsize=(12, 6))
plt.plot(data['Year'], signal, label='Well Depth')

#overlay vertical lines at detected change points
for bp in breakpoints[:-1]:  #
    plt.axvline(x=data['Year'].iloc[bp], color='red', linestyle='--', label='Change Point' if bp == breakpoints[0] else "")

#just labeling the graph
plt.xlabel('Year')
plt.ylabel('Well Depth (m)')
plt.title("Ogallala Well Depth with Detected Change Points")
plt.legend()
plt.show()
