#import libraries
from CI_Final import analyze_aquifer_data_CI
from histogram_plot import plot_histogram
from n_value import analyze_aquifer_data_n
from change_point_git import analyze_aquifer_data_CP
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np



# Test a function
aquifer_file = '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'

# Create a 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Call your functions, but pass in the axis you want to draw on
analyze_aquifer_data_CI(aquifer_file, 'Ogallala', 1920, 2023, ax=axs[0,0])
axs[0,0].set_title("Theil-Sen Regression Plot", fontsize=18)

analyze_aquifer_data_CP(aquifer_file, 'Ogallala', 1920, 2023, None, [1968, 1987, 2023], ax=axs[0,1])

axs[0,1].set_title("Change Point Analysis", fontsize=18)

plot_histogram(aquifer_file, 'Ogallala', 1920, ax=axs[1,0])
axs[1,0].set_title("Histogram", fontsize=18)

analyze_aquifer_data_n(aquifer_file, 'Ogallala', 1920, 2023, ax=axs[1,1])
axs[1,1].set_title("N-Value", fontsize=18)

#set title
fig.suptitle('Ogallala Aquifer Analysis', fontsize=22)

# Adjust layout
plt.tight_layout()
plt.show()