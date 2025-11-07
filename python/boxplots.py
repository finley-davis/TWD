import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import theilslopes

#read in the data
file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
data = pd.read_csv(file_path)

#renaming columns
data.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16']
#This is for the 5 years after the date


#dt formatting, meaning it will only take the year
data['Date'] = pd.to_datetime(data['Date'], format='%Y', errors='coerce')
#drop columns that are not needed
data = data.dropna(subset=['Date', 'Depth'])

#filtering out the data before 1930
data = data[data['Date'] >= pd.to_datetime("1930")]

#extract the year without using .dt
data['Year'] = data['Date'].dt.year
data['Depth'] = pd.to_numeric(data['Depth'], errors='coerce')


#I am grouping the data by 5 year intervals
#This is for the box plots
data['5_Year_Interval'] = (data['Year'] // 5) * 5
grouped = data.groupby('5_Year_Interval')['Depth']
#This is for the theil-sen regression
median_depths = grouped.median()
#This is for the box plots
intervals = median_depths.index

#for box plots, drop the NaN values
#dropna is commmon in pandas to remove missing values
depth_by_5_years = [group.dropna().values for _, group in grouped]


#plotting box and whisker plot
#figure with height of 12 inches and width of 8 inches
plt.figure(figsize=(12, 8))

#plotting box plot
#vert = True means that the box plot will be vertical
#patch_artist = False means that the box plot will not be filled with color
#positions = intervals means that the x-axis will be the intervals
plt.boxplot(depth_by_5_years, vert=True, patch_artist=False, positions=intervals)  # Use actual intervals for positions

#plotting the median line
#ticks = intervals means that the x-axis will be the intervals
#rotation = 45 means that the x-axis labels will be rotated 45 degrees
plt.xticks(ticks=intervals, labels=intervals, rotation=45)

#labeling the x-axis, y-axis, and title
plt.xlabel('5-Year Intervals')
plt.ylabel('Depth')
plt.title('Well Depth Distribution by 5-Year Intervals of the Ogallala Aquifer with Theil-Sen Trend Line')

#This is the median line
#color = 'blue' means that the line will be blue
#marker = 'o' means that the points will be circles
#linestyle = '-' means that the line will be solid
#label = 'Median Depths' means that the line will be labeled 'Median Depths' in the legend
plt.plot(intervals, median_depths.values, color='blue', marker='o', linestyle='-', label='Median Depths')


#Theil-Sen Regression function
def plot_theil_sen_regression(x, y):
    #theilslopes returns the slope, intercept, lower slope, and upper slope
    slope, intercept, lower_slope, upper_slope = theilslopes(y, x)
    #plots the line
    #x = x values
    #slope * np.array(x) + intercept = y values
    #color = 'red' means that the line will be red
    #label = f'Theil-Sen Line: y = {slope:.2f}x + {intercept:.2f}' means that the line will be labeled as the eqn. of the line
    plt.plot(x, slope * np.array(x) + intercept, color='red', label=f'Theil-Sen Line: y = {slope:.2f}x + {intercept:.2f}')
    #plots the shaded region
    print(f"Theil-Sen Regression Equation: Depth = {slope:.4f} * Interval + {intercept:.4f}")
    print(f"Slope Range: {lower_slope:.4f} to {upper_slope:.4f}")

#plotting again
plot_theil_sen_regression(intervals, median_depths.values)

#shows legend and plot
plt.legend()
plt.show()


#checking depths with print statemete
#this is just trouble shooting
#print(data.head(100))  #prints the first 100 rows