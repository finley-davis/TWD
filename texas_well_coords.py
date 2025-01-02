import geopandas as gpd
import matplotlib.pyplot as plt

#load Texas shapefile that I downloaded from https://github.com/johan/world.geo.json/blob/master/countries.geo.json
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json')

#create a GeoDataFrame for points
from shapely.geometry import Point

"""
aquifer_pathname = {'Ogallala': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv',
                    'Edwards (Balcones Fault Zone)': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv',
                    'Edwards-Trinity Plateau': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards-Trinity Plateau.csv',
                    'Carrizo-Wilcox': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Carrizo-Wilcox.csv',
                    'Gulf Coast': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Gulf Coast.csv',
                    'Pecos Valley': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Pecos Valley.csv',
                    'Seymour': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Seymour.csv',
                    'Trinity': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Trinity.csv',
                    'Hueco-Mesilla Basin': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Hueco-Mesilla Basin.csv'
                    }


aquifers = {'Ogallala': 'red',
            'Edwards (Balcones Fault Zone)': 'orange', 
            'Edwards-Trinity Plateau': 'yellow',
            'Carrizo-Wilcox': 'green',
            'Gulf Coast': 'blue',
            'Pecos Valley': 'indigo',
            'Seymour': 'violet',
            'Trinity': 'magenta',
            'Hueco-Mesilla Basin': 'pink'
            }
"""
            

#Ogallala points
ogallala = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv')
ogallala_coordinates = ogallala.iloc[:, [6, 7]].values
ogallala_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in ogallala_coordinates], crs="EPSG:4326")
#Edwards (Baclones Fault Zone) Aqufier points
edwardsbfz = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv')
edwardsbfz_coordinates = edwardsbfz.iloc[:, [6, 7]].values
edwardsbfz_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in edwardsbfz_coordinates], crs="EPSG:4326")
#Edwards-Trinity PLateau Aquifer points
edwardstp = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards-Trinity Plateau.csv')
edwardstp_coordinates = edwardstp.iloc[:, [6, 7]].values
edwardstp_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in edwardstp_coordinates], crs="EPSG:4326")
#Carrizo-Wilcox Aquifer points
carrizowilcox = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Carrizo-Wilcox.csv')
carrizowilcox_coordinates = carrizowilcox.iloc[:, [6, 7]].values
carrizowilcox_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in carrizowilcox_coordinates], crs="EPSG:4326")
#Gulf Coast Aquifer points
gulfcoast = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Gulf Coast.csv')
gulfcoast_coordinates = gulfcoast.iloc[:, [6, 7]].values
gulfcoast_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in gulfcoast_coordinates], crs="EPSG:4326")
#Pecos Valley Aquifer points
pecosvalley = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Pecos Valley.csv')
pecosvalley_coordinates = pecosvalley.iloc[:, [6, 7]].values
pecosvalley_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in pecosvalley_coordinates], crs="EPSG:4326")
#Seymour Aquifer points
seymour = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Seymour.csv')
seymour_coordinates = seymour.iloc[:, [6, 7]].values
seymour_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in seymour_coordinates], crs="EPSG:4326")
#Trinity Aquifer points
trinity = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Trinty.csv')
trinity_coordinates = trinity.iloc[:, [6, 7]].values
trinity_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in trinity_coordinates], crs="EPSG:4326")
#Hueco-Mesilla Basin Aquifer points
hmb = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Hueco-Mesilla Basin.csv')
hmb_coordinates = hmb.iloc[:, [6, 7]].values
hmb_points = gpd.GeoDataFrame(geometry=[Point(x[1], x[0]) for x in hmb_coordinates], crs="EPSG:4326")


#plots map of Texas
fig, ax = plt.subplots(figsize=(10, 10))
texas.plot(ax=ax, color='lightblue', edgecolor='black')

#plots aquifer points
#starts with Ogallala in red
ogallala_points.plot(ax=ax, color='red', markersize=5)
#then Edwards (Balcones Fault Zone) in orange
edwardsbfz_points.plot(ax=ax, color='orange', markersize=5)
#then Edwards-Trinity Plateau in yellow
edwardstp_points.plot(ax=ax, color='yellow', markersize=5)
#then Carrizo-Wilcox in green
carrizowilcox_points.plot(ax=ax, color='green', markersize=5)
#then Gulf Coast in blue
gulfcoast_points.plot(ax=ax, color='blue', markersize=5)
#then Pecos Valley in purple
pecosvalley_points.plot(ax=ax, color='indigo', markersize=5)
#then Seymour in indigo
seymour_points.plot(ax=ax, color='violet', markersize=5)
#then Trinity in violet
trinity_points.plot(ax=ax, color='magenta', markersize=5)
#then Hueco-Mesilla Basin in pink
hmb_points.plot(ax=ax, color='pink', markersize=5)


plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid()
plt.tight_layout()
plt.legend(title="Aquifer Well Points", labels=["Ogallala Aquifer", "Edwards (Balcones Fault Zone) Aquifer", "Edwards-Trinity Plateau Aquifer",
            "Carrizo-Wilcox Aquifer", "Gulf Coast Aquifer", "Pecos Valley Aquifer", "Seymour Aquifer",
            "Trinity Aquifer", "Hueco-Mesilla Basin Aquifer"])
plt.title("Map of Texas with Well Points Delineated by Aquifer")
plt.show()

