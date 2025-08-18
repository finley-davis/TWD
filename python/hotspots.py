#hotspots

#how should I do this?
#This script is intended to analyze hotspot data and generate reports.
#It will read in data, process it, save the results to a CSV file, and output an image.

#There must be some relation between closeness and magnitude
#imports
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, box
from scipy.stats import theilslopes
import contextily as ctx

#load data
df = pd.read_csv("/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv")

#clean columns
df.columns = df.columns.str.strip()
df = df.rename(columns={"Date": "Year", "Depth": "Depth_ft"})
df = df.dropna(subset=["Latitude", "Longitude", "Year", "Depth_ft"])

#converts gdf to the appropriate coordiante ref system (EPSG:3857)
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
    crs="EPSG:4326"
).to_crs("EPSG:3857")

#loads texas shp
texas = gpd.read_file('/Users/finleydavis/Desktop/Cardenas Research/Python/Texas_Map/TX.geo.json').to_crs("EPSG:3857")

#Texas grid estimate (fix later)
xmin, ymin, xmax, ymax = texas.total_bounds
grid_size = 50000  # 50 km grid cells
cols = np.arange(xmin, xmax + grid_size, grid_size)
rows = np.arange(ymin, ymax + grid_size, grid_size)
polygons = [box(x, y, x + grid_size, y + grid_size) for x in cols for y in rows]
grid = gpd.GeoDataFrame({'geometry': polygons}, crs="EPSG:3857")

#join wells to grid cells
joined = gpd.sjoin(gdf, grid, how="inner", predicate="within")

#estimate slope of depth change over time in each grid cell using T-S estimator
results = []
for idx, cell in grid.iterrows():
    wells_in_cell = joined[joined.index_right == idx]
    if len(wells_in_cell) >= 3:
        years = wells_in_cell["Year"].astype(float)
        depths = wells_in_cell["Depth_ft"].astype(float)
        try:
            slope, intercept, _, _ = theilslopes(depths, years)
            results.append({
                "geometry": cell.geometry,
                "slope": slope
            })
        except Exception:
            continue

#creates gdf from slope results
slopes_gdf = gpd.GeoDataFrame(results, crs=grid.crs)

#clip to tex boundary
slopes_gdf = gpd.overlay(slopes_gdf, texas, how="intersection")

#plot
fig, ax = plt.subplots(figsize=(10, 7))
slopes_gdf.plot(
    column="slope",
    cmap="RdBu_r",
    legend=True,
    edgecolor="black",
    legend_kwds={"label": "Change in Depth (ft/year)", "shrink": 0.6},
    ax=ax
)
gdf.plot(ax=ax, color="black", markersize=5, alpha=0.3, label='Wells')
texas.boundary.plot(ax=ax, edgecolor="gray", linewidth=1.2)

#basemap
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=gdf.crs, zoom=7)

#title/layout
ax.set_title("Estimated Groundwater Depth Change Rate Across Texas (ft/year)", fontsize=14)
ax.axis('off')
plt.tight_layout()
plt.show()