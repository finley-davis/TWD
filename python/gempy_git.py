#gempy 

import gempy as gp
import gempy_viewer as gpv

# Importing aux libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

from gempy_engine.config import AvailableBackends
from gempy.core.data import Grid
from gempy.core.data.grid_modules import RegularGrid


#read in the data
file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Edwards (Balcones Fault Zone) Aquifer.csv'
data = pd.read_csv(file_path)

#renaming columns
data.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16']# 'Unnamed17', 'Unnamed18']
#This is for the 5 years after the date


#creating a model
geo_model = gp.create_geomodel()







