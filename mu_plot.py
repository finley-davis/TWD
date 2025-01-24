import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

start_year = 1920
end_year = 2020

file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
df = pd.read_csv(file_path)

df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
              'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 
              'Unnamed16']

df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')
df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]

df['Year'] = df['Date'].dt.year
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
df = df.dropna(subset=['Depth'])

bins = list(range(start_year, end_year + 1, 5))
labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins) - 1)]
df['Year_Bin'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)

plt.figure(figsize=(15, 10))

year_bins = sorted([bin for bin in df['Year_Bin'].unique() if not pd.isna(bin)])
x_positions = np.arange(len(year_bins))

max_depth = df['Depth'].max()
min_depth = df['Depth'].min()
bin_edges = np.linspace(min_depth, max_depth, 50)

mu_values = []
for i, year_bin in enumerate(year_bins):
    subset = df[df['Year_Bin'] == year_bin]
    depth_data = subset['Depth'].values
    hist, _ = np.histogram(subset['Depth'], bins=bin_edges, density=True)
    hist = hist / hist.max() * 0.4

    #uncomment below to plot the histogram
    #plt.barh(bin_edges[:-1], -hist, height=np.diff(bin_edges), left=x_positions[i], color='red')
    #plt.barh(bin_edges[:-1], hist, height=np.diff(bin_edges), left=x_positions[i], color='red')

    if len(depth_data) > 0:
        log_depth = np.log(depth_data)
        mu = log_depth.mean()
        mu_depth = np.exp(mu)
        mu_values.append((x_positions[i], mu_depth))
        plt.plot([x_positions[i] - 0.4, x_positions[i] + 0.4], [mu_depth, mu_depth], color='black', linestyle='-', linewidth=2)
        plt.text(x_positions[i], mu_depth + 5, f'mu = {mu_depth:.2f}', ha='center', color='black', fontsize=7.5)
        


plt.ylim(0, max_depth)
x_mu, y_mu = zip(*mu_values)
slope, intercept, _, _, _ = linregress(x_mu, y_mu)
trend_line = np.array(x_mu) * slope + intercept
plt.plot(x_mu, trend_line, color='blue', linestyle='-', linewidth=2, label='Trend Line')

plt.title('Ogallala Aquifer Depth Distribution with Lognormal Means and Trend Line (1920-2020)', pad=20)
plt.xlabel('Year Interval')
plt.ylabel('Depth (ft)')
plt.xticks(x_positions, year_bins, rotation=45, ha='right')
plt.grid(True, axis='y', linestyle='--')
plt.legend()
plt.tight_layout()

plt.show()

    