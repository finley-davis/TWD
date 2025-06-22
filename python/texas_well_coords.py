import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# load Texas shapefile
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json')

# dictionary of aquifers with color and path to data
aquifers = {
    'Ogallala': {
        'color': 'lightblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'
    }#,
}
"""
    'Edwards (Balcones Fault Zone)': {
        'color': 'darkblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards (Balcones Fault Zone) Aquifer)_Final.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'lightgreen',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards-Trinity Plateau_Final.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/csvs final/Carrizo-Wilcox_Final.csv'
    },
    'Gulf Coast': {
        'color': 'yellow',
        'path': '/Users/finleydavis/Desktop/csvs final/Gulf Coast_Final.csv'
    },
    'Pecos Valley': {
        'color': 'orange',
        'path': '/Users/finleydavis/Desktop/csvs final/Pecos Valley_Final.csv'
    },
    'Seymour': {
        'color': 'brown',
        'path': '/Users/finleydavis/Desktop/csvs final/Seymour_Final.csv'
    },
    'Trinity': {
        'color': 'green',
        'path': '/Users/finleydavis/Desktop/csvs final/Trinty_Final.csv'
    },
    'Hueco-Mesilla Basin': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/csvs final/Hueco-Mesilla Basin_Final.csv'
    }
"""
#}

# plot Texas base map
fig, ax = plt.subplots(figsize=(9, 6))
texas.plot(ax=ax, color='#F5DEB3', edgecolor='black')  # wheat (lighter tan)

# list for legend and counter for total points
legend_labels = []
total_points = 0

# loop through aquifers
for name, info in aquifers.items():
    # read CSV using pandas
    df = pd.read_csv(info['path'])
    
    # extract coordinates from correct columns (Latitude: col 1, Longitude: col 2)
    coordinates = df.iloc[:, [1, 2]].dropna().values
    
    # convert to GeoDataFrame
    points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in coordinates], crs="EPSG:4326")
    
    # plot aquifer well points
    points.plot(ax=ax, color=info['color'], markersize=0.1)
    
    # update legend and count
    legend_labels.append(f"{name} Aquifer")
    total_points += len(points)

# add map details
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid()
plt.tight_layout()
plt.legend(title="Aquifer Well Points", labels=legend_labels, markerscale=10)
plt.title("Map of Texas with Well Points Delineated by Aquifer")
plt.show()

# output total number of points
print(f"Total number of points plotted: {total_points}")
