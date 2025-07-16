# Updated code with:
# 1) Changing date display in the video
# 2) 2D depth bar showing min/max depth with moving dot for log mean depth

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize, to_hex
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from scipy.stats import gmean

# dictionary containing aquifer data
aquifers = {
    'Ogallala': {
        'color': 'Reds',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
    },
    'Edwards (Balcones Fault Zone)': {
        'color': 'Oranges',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'YlOrBr',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards-Trinity Plateau.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'Greens',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Carrizo-Wilcox.csv'
    },
    'Gulf Coast': {
        'color': 'Blues',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Gulf Coast.csv'
    },
    'Pecos Valley': {
        'color': 'indigo',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Pecos Valley.csv'
    },
    'Seymour': {
        'color': 'Purples',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Seymour.csv'
    },
    'Trinity': {
        'color': 'magenta',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Trinity.csv'
    },
    'Hueco-Mesilla Basin': {
        'color': 'Pinks',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Hueco-Mesilla Basin.csv'
    }
}
#
# Set up font for year display
year_font = FontProperties()
year_font.set_family('sans-serif')
year_font.set_weight('bold')
year_font.set_size(24)

start_year = 1900
end_year = 2020

def load_aquifer_data(filepath):
    df = pd.read_csv(filepath)
    df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                  'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16']
    
    df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    
    df['Year'] = df['Date'].dt.year
    df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
    df = df.dropna(subset=['Depth'])
    return df

df = load_aquifer_data(aquifers['Edwards-Trinity Plateau']['path'])

# Calculate depth range - using percentiles to handle outliers
depth_min = 0
depth_max = df['Depth'].quantile(0.95)  # Using 95th percentile as max to avoid extreme outliers

# Create figure with improved layout
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(1, 2, width_ratios=[5, 0.5], wspace=0.1)
ax = fig.add_subplot(gs[0], projection='3d')
ax_depth = fig.add_subplot(gs[1])

# Load Texas boundary
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json')

# Setup colormap - now using all individual years
years = sorted(df['Year'].unique())
norm = Normalize(vmin=min(years), vmax=max(years))
cmap = get_cmap('YlOrBr')

# Initialize depth bar
def init_depth_bar():
    ax_depth.clear()
    ax_depth.set_ylim(depth_max + 50, max(0, depth_min - 50))
    ax_depth.set_xlim(0, 1)
    ax_depth.axis('off')
    
    ax_depth.add_patch(Rectangle((0.4, depth_min), width=0.2,
                      height=depth_max - depth_min,
                      color='lightgray', alpha=0.6))
    
    ax_depth.text(0.8, depth_min, f'{int(depth_min)} ft', ha='left', va='center', fontsize=8)
    ax_depth.text(0.8, depth_max, f'{int(depth_max)} ft', ha='left', va='center', fontsize=8)
    ax_depth.text(0.5, depth_min - 30, 'Well Depth', ha='center', va='top', fontsize=10)

init_depth_bar()
depth_dot, = ax_depth.plot([0.5], [depth_min], 'ro', markersize=8)

# Initialize year display
year_text = fig.text(0.80, 0.92, "", ha='center', va='center', 
                    fontproperties=year_font, color='black',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Function to update the plot for each time step
def update_frame(i):
    current_year = years[i]
    
    # Update year display
    year_text.set_text(f"{current_year}")
    
    # Clear and update main plot
    ax.cla()
    ax.view_init(elev=10)
    
    # Plot Texas boundary
    for _, geom in texas.iterrows():
        surface_elevation = geom.get('elevation', 0)
        if geom.geometry.geom_type == 'Polygon':
            x, y = geom.geometry.exterior.xy
            ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)
        elif geom.geometry.geom_type == 'MultiPolygon':
            for polygon in geom.geometry.geoms:
                x, y = polygon.exterior.xy
                ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)
    
    # Plot all points up to the current year
    current_data = df[df['Year'] <= current_year]
    colors = [to_hex(cmap(norm(year))) for year in current_data['Year']]
    
    ax.scatter(
        current_data['Long'],
        current_data['Lat'],
        -current_data['Depth'],
        c=colors,
        s=0.5,
        alpha=0.8
    )
    
    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Depth (ft below surface)")
    ax.set_zlim(-depth_max - 50, 0)
    ax.set_title(f"Edwards-Trinity Plateau Aquifer Well Depths Over Time", pad=10)
    
    # Update depth bar
    init_depth_bar()
    
    # Calculate lognormal mean for current year
    current_year_data = df[df['Year'] == current_year]
    if not current_year_data.empty:
        # Using geometric mean as lognormal mean
        lognormal_mean = gmean(current_year_data['Depth'])
        depth_dot.set_data([0.5], [lognormal_mean])
        ax_depth.text(0.5, lognormal_mean + 30, 
                     f'Lognormal Mean:\n{lognormal_mean:.1f} ft', 
                     ha='center', va='bottom', color='red', fontsize=8)

# Create the animation - now using individual years
ani = animation.FuncAnimation(fig, update_frame, frames=range(len(years)), 
                             init_func=lambda: None, repeat=False)

# Display the plot
plt.tight_layout()
plt.show()

# Set up the writer and save the animation
writer = FFMpegWriter(fps=5, metadata={'title': 'Texas Aquifer Animation'}, bitrate=1800)  # Increased FPS for smoother animation
output_path = '/Users/finleydavis/Desktop/EdwardsTP_aquifer_animation_yearly.mp4'
ani.save(output_path, writer=writer)

print(f"Animation saved as {output_path}")