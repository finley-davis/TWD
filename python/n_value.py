# aquifer n-values
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress, theilslopes
import ruptures as rpt
from adjustText import adjust_text
from mpl_toolkits.axes_grid1.inset_locator import inset_axes  # For the inset chart

aquifers = {
    'Ogallala': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
    },
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
    'Hueco-Mesilla Bolsons': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Hueco-Mesilla Basin.csv'
    }
}

# Function to analyze and plot aquifer data with Theil-Sen trend, 10% CI, and n-values as an inset bar chart
def analyze_aquifer_data_n(file_path, aquifer_name, start_year=1920, end_year=2020, ax = None):
    # Load and clean data
    dtype = {'ID': 'int32', 'Lat': 'float32', 'Long': 'float32', 'County': 'category', 'Year': 'int16', 'Depth': 'float32'}
    chunks = pd.read_csv(file_path, chunksize=10000, dtype=dtype)
    df = pd.concat(chunks).reset_index(drop=True)
    df = df.dropna(axis=1, how='all')
    df.columns = ['ID', 'Lat', 'Long', 'County', 'Year', 'Depth']
    df = df[(df.Year.between(start_year, end_year)) & (df.Depth > 0)].copy()

    # Compute n-values (data points per year)
    yearly_counts = df.groupby('Year').size()

    #for fig
    if ax is None:
        fig, ax = plt.subplots()
    # Save n-values to an Excel sheet
    #yearly_counts.to_excel('/Users/finleydavis/Desktop/Cardenas Research/Excel/Slope Values/Aquifer_n_Values.xlsx', sheet_name='n_values')

    # Print n-values for each year
    print(f"\nNumber of data points per year: {yearly_counts}")
    #yearly_counts_tot = yearly_counts.append()
    #yearly_counts_tot.to_csv('/Users/finleydavis/Desktop/Aquifer_n_Values.csv', index=False)

    # Create an Excel writer outside the loop in append mode
    #with pd.ExcelWriter('/Users/finleydavis/Desktop/Cardenas Research/Excel/Slope Values/Aquifer_n_Values.xlsx', 
    #                    engine='openpyxl', mode='w') as writer:
    #    i = 0  # Initialize column index
    #    for year, count in yearly_counts.items():
    #        print(f"Year {year}: {count} data points")
    #
    #        # Convert yearly_counts to DataFrame
    #        df = yearly_counts.to_frame(name='n_values')
    #
    #        # Write to the Excel file at the correct column
    #        #df.to_excel(writer, sheet_name='n_values', startrow=1, startcol=i, index_label='Year')
    #
    #        #i += 3

    ax.bar(yearly_counts.index, yearly_counts.values, color='black', width=0.8)
    #ax.set_xlabel('Year')     #off for fig
    #ax.set_ylabel('Number of Data Points')     #off for fig
    #ax.set_title(f"{aquifer_name} Number of Data Points per Year")     #off for fig
    ax.grid(True)

    # Show the plot
    #plt.show()

#analyze_aquifer_data(aquifers['Ogallala']['path'], start_year=1920, end_year=2023)
#outputting all graphs into one folder for slides

safe_folder_name = "n_values_all_aquifers"

#create the output directory
#output_dir = f"/Users/finleydavis/Desktop/Figures{safe_folder_name}"   #off for fig
#os.makedirs(output_dir, exist_ok=True).     #off for fig

"""
#main loop to generate and save each aquifer plot
for name, data in aquifers.items():
    file_path = data['path']
    plt.figure()  #create a new figure for each aquifer
    analyze_aquifer_data_n(file_path, start_year=1920, end_year=2023)

    output_path = os.path.join(output_dir, f"{name}_n_values.pdf")
    #plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

"""