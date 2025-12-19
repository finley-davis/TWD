#for poster

#import libraries
from CI_Final import analyze_aquifer_data_CI
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

#import aq. paths
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

selected = [
    'Edwards-Trinity Plateau',
    'Carrizo-Wilcox',
    'Hueco-Mesilla Bolsons',
    'Pecos Valley',
    'Seymour',
    'Trinity'
]

fig, axs = plt.subplots(2, 3, figsize=(20, 10))
axs = axs.flatten()

for i, aquifer in enumerate(selected):
    ax = axs[i]
    print(f"Processing {aquifer}...")

    analyze_aquifer_data_CI(
        file_path=aquifers[aquifer]['path'],  # this argument isn't used, but keep structure
        aquifer_name=aquifer,
        start_date=1920,
        end_date=2023,
        ax=ax
    )

    ax.set_title(aquifer)   # Only include if desired

fig.text(0.03, 0.97, '(a)', fontsize=16, fontweight='bold')
fig.text(0.36, 0.97, '(b)', fontsize=16, fontweight='bold')
fig.text(0.695, 0.97, '(c)', fontsize=16, fontweight='bold')

fig.text(0.03, 0.48, '(d)', fontsize=16, fontweight='bold')
fig.text(0.36, 0.48, '(e)', fontsize=16, fontweight='bold')
fig.text(0.695, 0.48, '(f)', fontsize=16, fontweight='bold')

plt.tight_layout()
#plt.show()
plt.savefig('/Users/finleydavis/Desktop/poster_6fig.pdf', dpi=300)