import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


start_year = 1930
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

for i, year_bin in enumerate(year_bins):
    subset = df[df['Year_Bin'] == year_bin]

    hist, _ = np.histogram(subset['Depth'], bins=bin_edges)
 
    hist = hist / hist.max() * 0.4 

    plt.barh(bin_edges[:-1], -hist, height=np.diff(bin_edges), 
             left=i, alpha=0.6, color='skyblue')

    plt.barh(bin_edges[:-1], hist, height=np.diff(bin_edges), 
             left=i, alpha=0.6, color='skyblue')

plt.title('Ogallala Aquifer Depth Distribution (1930-2020)', pad=20)
plt.xlabel('Year Interval')
plt.ylabel('Depth')


plt.xticks(x_positions, year_bins, rotation=45, ha='right')

plt.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()

plt.show()