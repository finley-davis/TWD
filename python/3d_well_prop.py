import geopandas as gpd  # import geopandas for handling geospatial data
import matplotlib.pyplot as plt  # import matplotlib for plotting
import pandas as pd  # import pandas for data manipulation
from shapely.geometry import Point  # import Point from shapely for geometric operations
import numpy as np  # import numpy for numerical operations
from scipy.interpolate import griddata  # import griddata from scipy for interpolation
from mpl_toolkits.mplot3d import Axes3D  # import Axes3D for 3d plotting
import matplotlib.animation as animation  # import animation for creating animations
from matplotlib.cm import get_cmap  # for colormap
from matplotlib.colors import Normalize, to_hex  # for normalizing and converting colors
from matplotlib.animation import FFMpegWriter  # for saving animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# dictionary containing aquifer data
aquifers = {
    'Ogallala': {
        'color': 'Reds',  # color for plotting
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'  # file path to aquifer data
    },
    'Edwards (Balcones Fault Zone)': {
        'color': 'Oranges',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'Yellows',
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

# predefined start and end years for the time period
start_year = 1900
end_year = 2020

# function that loads and processes aquifer data
def load_aquifer_data(filepath):
    df = pd.read_csv(filepath)  # read csv file into dataframe
    # rename columns for clarity
    df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                  'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16']
    
    df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')  # convert date column to datetime
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]  # filter data by date range
    
    # convert to numeric values and drop NaNs
    df['Year'] = df['Date'].dt.year  # extract year from date
    df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')  # convert depth to numeric
    df = df.dropna(subset=['Depth'])  # drop rows with NaN depth
    
    # create bins for 5-year interval
    bins = list(range(start_year, end_year + 1, 5))  # create list of bin edges
    labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins) - 1)]  # create labels for bins
    df['Year_Bin'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)  # bin the years
    
    return df  #return the processed dataframe

#load data for the ogallala aquifer
df = load_aquifer_data(aquifers['Edwards-Trinity Plateau']['path'])

#create figure and 3d axes
fig = plt.figure(figsize=(15, 12))  # create a figure
ax = fig.add_subplot(111, projection='3d')  # add a 3d subplot

#plot texas boundary (we can leave this static for now)
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json')  # read texas boundary data

# setup colormap
year_bins = sorted(df['Year_Bin'].dropna().unique())  # drop NaNs and sort bins
norm = Normalize(vmin=0, vmax=len(year_bins) - 1)  # normalize bin indices
cmap = get_cmap('YlOrBr')  # define colormap

#adding image to 
logo_path = '/Users/finleydavis/Desktop/Cardenas Research/Graph_pngs/Ogallala_depth_analysis.png'
logo_img = mpimg.imread(logo_path)

#function to update the plot for each time step (5-year interval)
def update_frame(i):
    current_label = year_bins[i]  #get the current bin label
    
    #clear the current frame
    ax.cla()  #clear the axes

    ax.view_init(elev=10)#,azim=270)  #change these values as needed

    #plot texas boundary again in 3d at z=0
    for _, geom in texas.iterrows():  #iterate over each geometry in texas
        surface_elevation = geom.get('elevation', 0)  #get surface elevation if available
        if geom.geometry.geom_type == 'Polygon':  #if geometry is a polygon
            x, y = geom.geometry.exterior.xy  #get x and y coordinates
            ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)  # plot the polygon
        elif geom.geometry.geom_type == 'MultiPolygon':  #if geometry is a multipolygon
            for polygon in geom.geometry.geoms:  #iterate over each polygon
                x, y = polygon.exterior.xy  #get x and y coordinates
                ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)  #plot the polygon
    
    #plot all points up to the current time bin with color gradient
    for j in range(i + 1):
        bin_label = year_bins[j]
        bin_data = df[df['Year_Bin'] == bin_label]
        color = to_hex(cmap(norm(j)))  #map year bin index to color
        ax.scatter(
            bin_data['Long'],  #longitude
            bin_data['Lat'],  #latitude
            -bin_data['Depth'],  #negative depth to show below surface
            color=color,  #color from gradient
            s=0.5,  #size of points
            alpha=0.8,  #transparency
            label=str(bin_label) if j == i else ""  #label only latest bin
        )
    
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  #adjust subplot parameters
    #set labels and limits for better visualization
    ax.set_xlabel("Longitude")  #set x-axis label
    ax.set_ylabel("Latitude")  #set y-axis label
    ax.set_zlabel("Depth (ft below surface)")  #set z-axis label
    ax.set_zlim(-2000, 0)  #set z-axis limits
    ax.set_title(f"3D Visualization of Texas Aquifer Well Depths (up to {current_label})", pad=0)  #set plot title with adjusted padding

    imagebox = OffsetImage(logo_img, zoom=0.1)
    ab = AnnotationBbox(imagebox, (0.9, 0.9), xycoords='axes fraction', frameon=False)
    #ax.add_artist(ab)

#create the animation
ani = animation.FuncAnimation(fig, update_frame, frames=range(len(year_bins)), repeat=False)  #create animation

#display the plot
plt.tight_layout()  #adjust layout
plt.show()  #show the plot

#set up the writer with desired framerate and codec
writer = FFMpegWriter(fps=3, metadata={'title': 'Texas Aquifer Animation'}, bitrate=1800)

#save the animation
output_path = '/Users/finleydavis/Desktop/EdwardsTP_aquifer_animation.mp4'
ani.save(output_path, writer=writer)

print(f"Animation saved as {output_path}")
