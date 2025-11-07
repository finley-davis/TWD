import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress, theilslopes
from scipy import stats
import ruptures as rpt
from adjustText import adjust_text
from mpl_toolkits.axes_grid1.inset_locator import inset_axes  #for n chart, may not need

#dictioanry with aquifer names, colors, and file paths
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

#dictionary with y-limits for each aquifer, used for plotting
aquifer_ylim = {
    'Ogallala': (800, 0),
    'Edwards (Balcones Fault Zone)': (2000, 0),
    'Edwards-Trinity Plateau': (1000, 0),
    'Carrizo-Wilcox': (1500, 0),
    'Gulf Coast': (1500, 0),
    'Pecos Valley': (1400, 0),
    'Seymour': (300, 0),
    'Trinity': (1500, 0),
    'Hueco-Mesilla Bolsons': (1500, 0)
}
#dictionary with change points for each aquifer, used for plotting
aquifer_CP = {
    'Ogallala': [1968, 1987, 2023],    #testing slope change from 1980-2000-2020, idea from Jasechko et al., 2024
    'Edwards (Balcones Fault Zone)': [1955, 1980, 2023],
    'Edwards-Trinity Plateau': [1969, 1986, 2023],
    'Carrizo-Wilcox': [1944, 1987, 2023],
    'Gulf Coast': [1949, 1965, 2023],
    'Pecos Valley': [1973, 2007, 2023],
    'Seymour': [1976, 2016],
    'Trinity': [1958, 1969, 2003, 2023],
    'Hueco-Mesilla Bolsons': [1950, 2021]
}

#manual change points to examine time periods rather than algorithmically detected change points
#It seems to be that once you enter the 21st century, there is not enough data points for a reliable trend
aquifer_1980_2020_CP = [2000, 2023]

#name = 'Ogallala'
#file path, forget the color coding for this code
#file_path = aquifers[name]['path']


#perhaps change this to a rolling_bootstrap_theil_sen function?
def bootstrap_theil_sen(x, y, n_bootstrap=1000, ci=0.10):
    slopes = []
    
    #bootstrap resampling
    for _ in range(n_bootstrap):
        idx = np.random.choice(len(x), len(x), replace=True)  
        sample_x, sample_y = x[idx], y[idx]
        slope, _, _, _ = theilslopes(sample_y, sample_x)
        slopes.append(slope)
    
    #computing 10% confidence interval percentiles
    lower_bound = np.percentile(slopes, (50 - ci * 50))  # 45th 
    upper_bound = np.percentile(slopes, (50 + ci * 50))  # 55th 
    
    return lower_bound, upper_bound


#function to analyze and plot aquifer data with Theil-Sen trend, 10% CI, and n-values as an inset bar chart
def analyze_aquifer_data_CP(file_path, aquifer_name, start_year, end_year, output_folder=None, manual_change_points=None, ax = None):
    if output_folder is None:
        output_folder = '/Users/finleydavis/Desktop/ADD'
    
    #load data
    dtype = {'ID': 'int32', 'Lat': 'float32', 'Long': 'float32', 'County': 'category', 'Year': 'int16', 'Depth': 'float32'}
    chunks = pd.read_csv(file_path, chunksize=10000, dtype=dtype)
    df = pd.concat(chunks).reset_index(drop=True)
    df = df.dropna(axis=1, how='all')
    df.columns = ['ID', 'Lat', 'Long', 'County', 'Year', 'Depth']
    df = df[(df.Year.between(start_year, end_year)) & (df.Depth > 0)].copy()

    #computing n-values (data points per year)
    yearly_counts = df.groupby('Year').size()

    #print n-values for each year
    print("\nNumber of data points per year:")
    for year, count in yearly_counts.items():
        print(f"Year {year}: {count} data points")
    with pd.ExcelWriter('/Users/finleydavis/Desktop/Cardenas Research/Excel/Slope Values/Aquifer_n_Values.xlsx', engine='openpyxl', mode='w') as writer:
        yearly_counts.to_frame(name='n_values').to_excel(writer, sheet_name='n_values', startrow=0, startcol=0, index_label='Year')

    #calculating annual lognormal means
    def lognormal_mean(x):
        if len(x) == 1:
            return x.iloc[0]
        log_x = np.log(x)
        return np.exp(log_x.mean() + 0.5 * log_x.std() ** 2)

    annual_means = df.groupby('Year')['Depth'].agg(lognormal_mean).interpolate().reset_index()
    years = annual_means['Year'].values
    means = annual_means['Depth'].values

    min_ln_mean = np.min(means)
    min_ln_mean_year = years[np.argmin(means)]
    print(f'minimum ln-mean of: {min_ln_mean:.2f} for {aquifer_name} in {start_year}-{end_year}: {min_ln_mean_year}')

    max_ln_mean = np.max(means)
    max_ln_mean_year = years[np.argmax(means)]
    print(f'maximum ln-mean of: {max_ln_mean:.2f} for {aquifer_name} in {start_year}-{end_year}: {max_ln_mean_year}')

    #print total number of data points
    total_data_points = len(df)
    print(f"\nTotal number of data points for {aquifer_name} in {start_year}-{end_year}: {total_data_points}")

    if len(means) < 2:
        print(f"Insufficient data for {aquifer_name}. Skipping change point detection.")
        return  #skip change point analysis if not enough data points

    if manual_change_points is not None:
        change_points = [np.searchsorted(years, cp_year) for cp_year in manual_change_points]
        print(f"Using manually specified change points for {aquifer_name}: {manual_change_points}")
    else:
        #shaping the previous 1D array of means into a 2D array for CPD, necessary for ruptures library
        signal = means.reshape(-1, 1)
        #checking for NaN values in the signal, essentially asking if the there is even a need for change point detection
        if np.var(signal) < 1e-5:
            print(f"Low variance in signal for {aquifer_name}. Skipping change point detection.")
            return  #skip if the variance is too low
        
        #how sensitive the algorithm is to change points
        #np.var is the variance of the signal, which is used to determine the penalty for change point detection
        pen = max(1000, 0.1 * np.var(signal))

        try:
            #running change point detection only if there are enough data points
            #NOTE: Pruned Exact Linear Time (PELT), which detects multiple change points
            #l2 refers to least squares loss function, which detects means of the signal
            #min_size is the minimum size of a segment to be considered a change point
            #jump is the number of points to skip when searching for change points
            #.fit is sending the log-normal means tot he algorithm
            #.predict is returning the change points
            algo = rpt.Pelt(model="l2", min_size=20, jump=1).fit(signal)
            change_points = algo.predict(pen=pen)
        except ValueError as e:
            print(f"Error in change point detection for {aquifer_name}: {e}")
            return  #skip if an error occurs in change point detection

    #computing Theil-Sen slope
    slope, intercept, _, _ = theilslopes(means, years)
    lower_slope, upper_slope = bootstrap_theil_sen(years, means, ci=0.10)


    #creating figure
    #fig, ax = plt.subplots(figsize=(12, 7))

    #scatter plot of data points
    ax.scatter(df.Year, df.Depth, s=5, alpha=0.1, c=df.Depth, cmap='viridis') #, label=f'Data Points (n={len(df):,})')

    #annual means plot
    ax.plot(years, means, 'ko-', markersize=4)#, label='Annual Means', zorder=4)

    # Theil-Sen Trend Line
    #ax.plot(years, years * slope + intercept, '--', color='red', lw=2)#, label=f'Theil-Sen Trend: {slope:.2f} ft/yr')
    
    #segment analysis for change points
    prev_cp = 0
    for i, cp in enumerate(change_points):
        if cp >= len(years):
            continue

        seg_years = years[prev_cp:cp]
        seg_means = means[prev_cp:cp]

        #skipping short segments
        if len(seg_years) < 2:
            prev_cp = cp
            continue

        #computing Theil-Sen slope for the segment
        seg_slope, seg_intercept, _, _ = theilslopes(seg_means, seg_years)

        #plotting the trend line for this segment
        ax.plot(seg_years, seg_years * seg_slope + seg_intercept,
                linestyle='--', lw=2, label=f'Segment {i+1}: {seg_slope:.2f} ft/yr')

        #drawing vertical line at change point (except last point)
        if i < len(change_points) - 1:
            cp_year = years[cp]
            if i == 0:  #add label only for the first vertical line
                ax.axvline(cp_year, color=aquifers[aquifer_name]['color'], linestyle='--', alpha=1, label='Change Point')
            else:
                ax.axvline(cp_year, color=aquifers[aquifer_name]['color'], linestyle='--', alpha=1)

            #add text box with the year of the change point
            ax.text(cp_year, max(means) * 1.1, f'{int(cp_year)}', color='black',#aquifers[aquifer_name]['color'],
                     fontsize=10, ha='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        print(f"Segment {i+1} ({seg_years[0]}–{seg_years[-1]}): {seg_slope:.2f} ft/yr")
        prev_cp = cp
    
    #print the year with the most data points
    max_year = yearly_counts.idxmax()
    max_count = yearly_counts.max()
    print(f"\nYear with the most data points: {max_year} ({max_count} data points)")
    #print year with the least data points
    min_year = yearly_counts.idxmin()
    min_count = yearly_counts.min()
    print(f"Year with the least data points: {min_year} ({min_count} data points)")

    #print the years in which there are no data points


    #formatting
    
    #ax.set_title(f'{aquifer_name} Aquifer Depth Analysis: {start_year}-{end_year}\nTheil-Sen Trends with Changepoint Detection', pad=20)
    #ax.set_xlabel('Year')
    #ax.set_ylabel('Depth (ft)')
    ax.set_ylim(*aquifer_ylim[aquifer_name])
    ax.grid(alpha=0.2)
    ax.legend(loc='upper right')

    #inset Bar Chart for n-values, removed for now
    """
    ax_inset = inset_axes(ax, width="25%", height="25%", loc='upper center', borderpad=1.5)  # Create inset axes
    ax_inset.bar(yearly_counts.index, yearly_counts.values, color='gray', alpha=0.7)
    ax_inset.set_title("n-Values per Year", fontsize=10)
    ax_inset.set_xlabel("Year", fontsize=8)
    ax_inset.set_ylabel("Count", fontsize=8)
    ax_inset.tick_params(axis='both', which='major', labelsize=8)
    ax_inset.set_xticks(yearly_counts.index[::10])  # Show every 10 years for readability
    ax_inset.set_xticklabels(yearly_counts.index[::10], rotation=45)
    """
    #output path stuff for all aquifers 
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    """
    #NOTE: save the plot as a PDF in the specified folder
    #output_path = os.path.join(output_folder, f'{aquifer_name}_CP_analysis.pdf')
    #plt.savefig(output_path, format='pdf')

    #showing the plot
    #plt.show()

#NOTE:uncomment the following lines to run the function for all aquifers

""""
output_folder = '/Users/finleydavis/Desktop/ADD'
for aquifer_name, properties in aquifers.items():
    file_path = properties['path']
    color = properties['color']
    
    # Call the function for each aquifer
    analyze_aquifer_data_CP(file_path, aquifer_name, start_year=1920, end_year=2023, manual_change_points= aquifer_CP[aquifer_name], output_folder=output_folder)

"""

"""
#call this function to analyze a specific aquifer, for example the Ogallala
analyze_aquifer_data_-p;;l.CP(file_path = aquifers['Hueco-Mesilla Bolsons']['path'], 
                    aquifer_name = 'Hueco-Mesilla Bolsons', 
                    start_year=1920, 
                    end_year=2023, 
                    #uncomment the following line to save the output in a specific folder
                    #output_folder='/Users/finleydavis/Desktop/Cardenas Research/Graph_pngs/All Aquifers/05:09:2025 CP Analysis',
                    manual_change_points=aquifer_CP['Hueco-Mesilla Bolsons'],
                    #uncomment the following line to use the manual change points 1980-2020
                    #manual_change_points = aquifer_1980_2020_CP

)
"""
