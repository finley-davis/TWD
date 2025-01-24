#This must be adjusted for topographic values as it is "ft below surface"
#gonna have to go back through all the TWDB files and add the land surface elevation values
#after I'll subtract the depth value from land surface elev. for actual well depth rel. to sea level
#will also have to interpolate the land surface elev. values to make an accurate surface map (no idea how to do this yet)

#also need to fix this for correct aquifer data, this means I need to go back and fix the aquifer data (currently it is just coords
#and needs to remove data without depth and date values


import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import numpy as np
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D

#streamlined method (relative to earlier made methods) to load and process aquifer data
aquifers = {
    'Ogallala': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
    },
}
"""
    'Edwards (Balcones Fault Zone)': {
        'color': 'orange',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'yellow',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards-Trinity Plateau.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'green',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Carrizo-Wilcox.csv'
    },
    'Gulf Coast': {
        'color': 'blue',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Gulf Coast.csv'
    },
    'Pecos Valley': {
        'color': 'indigo',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Pecos Valley.csv'
    },
    'Seymour': {
        'color': 'violet',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Seymour.csv'
    },
    'Trinity': {
        'color': 'magenta',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Trinty.csv'
    },
    'Hueco-Mesilla Basin': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Hueco-Mesilla Basin.csv'
    }
}
"""
#experimenting w/ ogallala aquifer data

#function that loads and processes aquifer data
def load_aquifer_data(self, filepath):
    #load data from CSV file, filepath is used later when calling this function
    df = pd.read_csv(filepath)
    coordinates = df.iloc[:, [6, 7]].values
    #depths are in the 14th column, this is used to create a GeoDataFrame
    #iloc is used to select the 14th column by its index, and .values is used to convert the column to a NumPy array
    depth = df.iloc[:, 13].values  
    #create a GeoDataFrame with the coordinates and depths
    points = gpd.GeoDataFrame(
        #create a Point object for each coordinate pair, this is from shapely.geometry library
        #points are created with the latitude (y) as the first argument and longitude (x) as the second argument   
        geometry=[Point(x[1], x[0]) for x in coordinates],
        #set the reference system to EPSG:4326, which is the standard for latitude and longitude coordinates
        crs="EPSG:4326",
        #create a DataFrame with the depth values
        data={'depth': depth}
    )
    #return GDF with the points and depths
    return points

total_points = 0
for aquifer_name, properties in aquifers.items():
    #load aquifer data using the load_aquifer_data function created earier
    #returns GDF with the points and depths
    points = load_aquifer_data(aquifer_name, properties['path'])
    #plot the points in 3D
    if points is not None:
        num_points = len(points)
    print(f"{aquifer_name} Aquifer: {num_points} points plotted")
    total_points += num_points
#sum of total points
print(f"Total points plotted: {total_points}")

#loads texas boundary data I downloaded from github
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json')

#create figure and 3D axes
#15x12 is larger than I have used for other plots, this is to make the plot easier to read
fig = plt.figure(figsize=(15, 12))
#add_subplot is used to create a 3D plot, the 111 argument is used to create a single subplot
#111 means 1 row, 1 column, and first subplot
#projection='3d' is used to create a 3D plot
ax = fig.add_subplot(111, projection='3d')

#plot Texas boundary in 3D at z=0 (surface)
#this is the 3d alternative to this 
"""
fig, ax = plt.subplots(figsize=(10, 10))
texas.plot(ax=ax, color='lightblue', edgecolor='black')
"""
#just trying this out






#which was used in the 2d plot


#this now has some extra bulk that is not needed as I'm not making the surface elevation here
for index, geom in texas.iterrows():
    surface_elevation = texas.iloc[index]['elevation'] if 'elevation' in texas.columns else 0
    #plot each polygon in the MultiPolygon
    #geom is a MultiPolygon object, which is a collection of Polygon objects, so I iterate over each Polygon object
    #geom_type is used to check if the object is a Polygon or MultiPolygon
    if geom.geometry.geom_type == 'Polygon':
        x, y = geom.geometry.exterior.xy
        ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)
    elif geom.geometry.geom_type == 'MultiPolygon':
    # Loop through each polygon in the MultiPolygon
        for polygon in geom.geometry.geoms:
            x, y = polygon.exterior.xy
            ax.plot(x, y, np.full_like(x, surface_elevation), color='black', linewidth=1)




#plot each aquifer's points
#aquifers is a dictionary with the aquifer names as keys and the properties as path names and colors as values
for aquifer_name, properties in aquifers.items():
    #load aquifer data using the load_aquifer_data function created earier
    #returns GDF with the points and depths
    #aquifer_name is from the dictionary keys, and properties['path'] is the path to the CSV file
    points = load_aquifer_data(aquifer_name, properties['path'])
    #plot the points in 3D
    if points is not None:
        #plots as scatter points, may change this later
        ax.scatter(
            #x, y, and z coordinates are extracted from the geometry column of the GDF
            points.geometry.x,
            points.geometry.y,
            -points['depth'], #depth is negative to show below the surface
            color=properties['color'], #color is from the dictionary values
            label=f"{aquifer_name} Aquifer", #label is the aquifer name, maps to dictionary keys
            s=0.1, #size of the points
            alpha=0.6 #transparency of the points
        )


ax.set_zlim(-2000, 0) #sets the z-axis limits to show the depth below the surface


#setting labels 
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Depth (ft below surface)")

#invert z-axis ticks to show positive numbers
#this is used to show the depth as positive numbers, which I thought would look better
zlim = ax.get_zlim()
ax.set_zlim(zlim[0], zlim[1])
current_ticks = ax.get_zticks()
ax.set_zticklabels([int(abs(x)) for x in current_ticks])

#sets title
ax.set_title("3D Visualization of Texas Aquifer Well Depths", pad=20)

#legend for the aquifer well points
ax.legend(
    #title of the legend
    title="Aquifer Well Points",
    #title font size
    bbox_to_anchor=(1.15, 0.5),
    #title location
    loc='center left',
    #font size of the legend
    borderaxespad=0.,
    markerscale=10

)

#viewing angle of the 3d plot, sets initial viewpoint
ax.view_init(elev=20, azim=225)

#add a light gray surface at z=0 to represent the ground surface
xmin, xmax = ax.get_xlim()
ymin, ymax = ax.get_ylim()
xx, yy = np.meshgrid(np.linspace(xmin, xmax, 2), np.linspace(ymin, ymax, 2))
zz = np.zeros_like(xx)  # Surface at z=0
ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')


#adjusts layout to prevent legend cutoff
plt.tight_layout()

#show the 3d plot
plt.show()