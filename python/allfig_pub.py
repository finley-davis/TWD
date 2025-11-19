#import libraries
from CI_Final import analyze_aquifer_data_CI
from histogram_plot import plot_histogram
from n_value import analyze_aquifer_data_n
from change_point import analyze_aquifer_data_CP
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

aquifers = {
    'Ogallala': {
        'color': 'lightblue',
        'path': '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'
    },
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
    'Hueco-Mesilla Bolsons': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/csvs final/Hueco-Mesilla Basin_Final.csv'
    }
}

#test a function
aquifer_file = aquifers['Ogallala']['path']

# Create a 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Call your functions, but pass in the axis you want to draw on
#No titles for pub, add these only for pres.
analyze_aquifer_data_CI(aquifer_file, 'Ogallala', 1920, 2023, ax=axs[0,0])
#axs[0,0].set_title("Theil-Sen Regression Plot", fontsize=18)

analyze_aquifer_data_CP(aquifer_file, 'Ogallala', 1920, 2023, None, [1968, 1987, 2023], ax=axs[0,1])

#axs[0,1].set_title("Change Point Analysis", fontsize=18)

plot_histogram(aquifer_file, 'Ogallala', 1920, ax=axs[1,0])
#axs[1,0].set_title("Histogram", fontsize=18)

analyze_aquifer_data_n(aquifer_file, 'Ogallala', 1920, 2023, ax=axs[1,1])
#axs[1,1].set_title("N-Value", fontsize=18)

#set title
#fig.suptitle('Ogallala Aquifer Analysis', fontsize=22) #no title for pub

#fix issue w overlapping subplots
plt.tight_layout(rect=[0.08, 0, 1, 0.95])
plt.subplots_adjust(left=0.50, wspace=0.5, hspace=0.4)

#add labels
fig.text(0.08, 0.985, '(a)', fontsize=16, fontweight='bold')
fig.text(0.55, 0.985, '(b)', fontsize=16, fontweight='bold')
fig.text(0.08, 0.515, '(c)', fontsize=16, fontweight='bold')
fig.text(0.55, 0.515, '(d)', fontsize=16, fontweight='bold')

#add y-axis label
fig.text(0.00, 0.5, 'Well Depth (m below land surface)',
         va='center', rotation='vertical', fontsize=18)

# Individual y-label for the N-value plot
axs[1,1].set_ylabel('Sample Size (n)', fontsize=14)


# Adjust layout
plt.tight_layout()
#plt.show()
plt.savefig('/Users/finleydavis/Desktop/Fall 25 Courses/Phys Hydro/Project/Ogallala.svg', dpi=300)