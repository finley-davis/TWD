import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#entered year for x-axis values
start_year = 2000
end_year = 2020

#reading in data
df = pd.read_csv('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/TWD Ogallala Excel CSV_parsed_datesorted.csv')

#renaming data based on columns
df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
              'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16', 'Unnamed17', 'Unnamed18']

#dropping unnecessary columns
df['Year'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce').dt.year
df = df.dropna(subset=['Year', 'Depth'])
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')


slope, intercept = np.polyfit(df['Year'], df['Depth'], 1)
print(f"Linear Regression Slope: {slope:.4f}")
print(f"Linear Regression Intercept: {intercept:.4f}")

x_vals = np.linspace(df['Year'].min(), df['Year'].max(), 100)
y_vals = intercept + slope * x_vals
plt.plot(x_vals, y_vals, color='cyan', linestyle='--', label='Linear Regression Line')

plt.hexbin(df['Year'], df['Depth'], gridsize=50, cmap='inferno_r')
plt.colorbar(label='Density')
plt.xlabel('Year')
plt.ylabel('Well Depth (m)')
plt.title('Well Depth in Relation to Time for the Seymour Aquifer')

plt.show()