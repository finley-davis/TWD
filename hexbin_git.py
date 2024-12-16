import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#entered year for x-axis values
start_year = 2000
end_year = 2020

#reading in data
df = pd.read_csv('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv')

#renaming data based on columns
df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
              'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16']#, 'Unnamed17', 'Unnamed18']

#dropping unnecessary columns
df['Year'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce').dt.year
df = df.dropna(subset=['Year', 'Depth'])
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')

#slope and intercept for linear regression
slope, intercept = np.polyfit(df['Year'], df['Depth'], 1)
#printing out the slope and intercept in the terminal
print(f"Linear Regression Slope: {slope:.4f}")
print(f"Linear Regression Intercept: {intercept:.4f}")

#plotting the data
#x values are the years, y values are the depths
x_vals = np.linspace(df['Year'].min(), df['Year'].max(), 100)
y_vals = intercept + slope * x_vals
#plotting the linear regression line
#color is cyan, linestyle is dashed, label is the name of the line
plt.plot(x_vals, y_vals, color='cyan', linestyle='--', label='Linear Regression Line')

#plots hexbin plot for year and depth
#gridsize is the number of hexagons in the x direction
#colormap is inferno reversed, with the _r making its color from light to dark
plt.hexbin(df['Year'], df['Depth'], gridsize=50, cmap='inferno_r')
#adding a colorbar to the plot to show concentration of data
plt.colorbar(label='Density')
#labels
plt.xlabel('Year')
plt.ylabel('Well Depth (m)')
plt.title('Well Depth in Relation to Time for the Seymour Aquifer')

plt.show()