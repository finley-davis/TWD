import pandas as pd
import numpy as np
from scipy.stats import lognorm
import matplotlib.pyplot as plt

#input parameters (years to filter data)
start_year = 1930
end_year = 1935


#load in file path
file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
df = pd.read_csv(file_path)

#rename columns based on csv file
df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
              'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 
              'Unnamed16', 'Unnamed17', 'Unnamed18']

#convert date column to datetime object
#this means these values are being converted to dates and can be manipulated as dates instead of text strings
df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')

#commenting out this below line since there are not any invalid dates
#this would be used for an unflitered dataset
#invalid_date_rows = df[df['Date'].isna()].index.tolist()

#converting to list of valid dates
valid_date_rows = df[df['Date'].notna()].index.tolist()

#this is the code that would be used for an unfiltered dataset to see which rows have invalid dates
"""
print(f"Rows with invalid dates: {len(invalid_date_rows)}")
print(f"Location of rows with invalid dates: {invalid_date_rows}")
print(f"Rows with valid dates: {len(valid_date_rows)}")
print(f"Location of rows with valid dates: {valid_date_rows}")
print(f"Rows with invalid depths: {df['Depth'].isna().sum()}")
df = df.dropna(subset=['Date'])
"""

#filtering the dataset to only include rows with valid dates listed above
df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]

#convert depth column to numeric values
#this means these values are being converted to numbers and can be manipulated as numbers instead of text strings, similar to above
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
#drop rows with NaN values in the depth column
df = df.dropna(subset=['Depth'])


#log normal distribution equation, just for notes
#Log normal dist - X = e^(\mu + \sigma * Z) where Z is a standard normal variable
#giving the data to the lognormal distsribution
depth_data = df['Depth'].values
#this is converting the data to log space
log_depth = np.log(depth_data)
#mu is mean, sigma is standard deviation
mu, sigma = log_depth.mean(), log_depth.std()

#this is converting the data back to normal space
#uses the inverse of the logarithm function, which is the exponential function
textstr = f'Estimated mu: {mu:.2f}\nEstimated sigma: {sigma:.2f}'
print(textstr)

#giving the x variable to the lognormal distribution
x = np.linspace(min(depth_data), max(depth_data), 100)
#this is the lognormal distribution function
pdf = lognorm.pdf(x, s=sigma, scale=np.exp(mu))

#plotting the data
plt.figure(figsize=(10, 6))
#depth_data is listed above, alpha is the transparency of the data, color is the color of the data, edgecolor is the color of the edges of the data
#bins refers to number of divisions used to group the histogram data
#density is the density of the data
#alpha - the frequency of the data in each bin is plotted
plt.hist(depth_data, bins=20, density=True, alpha=0.6, color='b', edgecolor='black')
#x is the x variable r is the color of the line
#pdf is the lognormal distribution function
#linewidth is the width of the line
#adding a vertical line for the mean of the depth data
plt.axvline(x=np.exp(mu), color='g', linestyle='--', linewidth=2, label='Mean Depth')

#adding text box with mu and sigma values
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.95, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', horizontalalignment='right', bbox=props)
#plotting the lognormal distribution function
plt.plot(x, pdf, 'r', linewidth=2)
#labels
plt.title(f'Ogallala Lognormal Distribution of Depth Data ({start_year}-{end_year})')
plt.xlabel('Depth')
plt.ylabel('Density')
plt.legend(['Lognormal PDF', 'Depth Data Histogram'])
plt.show()