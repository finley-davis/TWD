import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import theilslopes, linregress
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

aquifers = {
    'Ogallala': {
        'color': 'red',
        'path': '/Users/finleydavis/Desktop/csvs final/Ogallala_Final.csv'
    },
    'Edwards (Balcones Fault Zone)': {
        'color': 'orange',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards (Balcones Fault Zone) Aquifer)_Final.csv'
    },
    'Edwards-Trinity Plateau': {
        'color': 'lime',
        'path': '/Users/finleydavis/Desktop/csvs final/Edwards-Trinity Plateau_Final.csv'
    },
    'Carrizo-Wilcox': {
        'color': 'green',
        'path': '/Users/finleydavis/Desktop/csvs final/Carrizo-Wilcox_Final.csv'
    },
    'Gulf Coast': {
        'color': 'blue',
        'path': '/Users/finleydavis/Desktop/csvs final/Gulf Coast_Final.csv'
    },
    'Pecos Valley': {
        'color': 'indigo',
        'path': '/Users/finleydavis/Desktop/csvs final/Pecos Valley_Final.csv'
    },
    'Seymour': {
        'color': 'violet',
        'path': '/Users/finleydavis/Desktop/csvs final/Seymour_Final.csv'
    },
    'Trinity': {
        'color': 'magenta',
        'path': '/Users/finleydavis/Desktop/csvs final/Trinty_Final.csv'
    },
    'Hueco-Mesilla Basin': {
        'color': 'pink',
        'path': '/Users/finleydavis/Desktop/csvs final/Hueco-Mesilla Basin_Final.csv'
    }
}

aquifer_ylim = {
    'Ogallala': (800, 0),
    'Edwards (Balcones Fault Zone)': (2000, 0),
    'Edwards-Trinity Plateau': (1000, 0),
    'Carrizo-Wilcox': (1500, 0),
    'Gulf Coast': (1500, 0),
    'Pecos Valley': (1400, 0),
    'Seymour': (300, 0),
    'Trinity': (1500, 0),
    'Hueco-Mesilla Basin': (1500, 0)
}

def analyze_aquifer_data(file_path, aquifer_name, start_date, end_date, output_folder=None):
    file_path = aquifers[aquifer_name]['path']
    aquifer_color = aquifers[aquifer_name]['color']

    dtype = {'ID': 'int32', 'Lat': 'float32', 'Long': 'float32', 'County': 'category', 'Date': 'int16', 'Depth': 'float32'}
    chunks = pd.read_csv(file_path, chunksize=10000, dtype=dtype)
    df = pd.concat(chunks).reset_index(drop=True)
    df = df.dropna(axis=1, how='all')
    df.columns = ['ID', 'Lat', 'Long', 'County', 'Date', 'Depth']
    df = df[(df.Date.between(start_date, end_date)) & (df.Depth > 0)].copy()

    def lognormal_mean(x):
        if len(x) == 1:
            return x.iloc[0]
        log_x = np.log(x)
        return np.exp(log_x.mean() + 0.5 * log_x.std() ** 2)

    annual_means = df.groupby('Date')['Depth'].agg(lognormal_mean).interpolate().reset_index()
    Dates = annual_means['Date'].values
    means = annual_means['Depth'].values
    print(means)


    slope, intercept, _, _ = theilslopes(means, Dates, alpha=0.90)
    #slope, intercept, *_ = linregress(means, Dates)
    trend_line = intercept + slope * Dates


    #bootstrapping
    n_boot = 1000
    bootstrap_trends = np.zeros((n_boot, len(Dates)))

    for i in range(n_boot):
        sample_idx = np.random.choice(len(Dates), size=len(Dates), replace=True)
        sample_Dates = Dates[sample_idx]
        sample_means = means[sample_idx]
        boot_slope, boot_intercept, *_ = theilslopes(sample_means, sample_Dates)
        bootstrap_trends[i] = boot_intercept + boot_slope * Dates

    lower_ci = np.percentile(bootstrap_trends, 5, axis=0)
    upper_ci = np.percentile(bootstrap_trends, 95, axis=0)

    print(f"{aquifer_name} Theil-Sen slope: {slope:.4f}")
    print("90% Bootstrap CI computed.\n")


    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_ylim(aquifer_ylim[aquifer_name])
    ax.scatter(df.Date, df.Depth, s=5, alpha=0.1, c=df.Depth, cmap='viridis', label=f'Data Points (n={len(df):,})')
    ax.plot(Dates, means, 'ko-', markersize=4, label='Annual Lognormal Means', zorder=4)
    ax.plot(Dates, trend_line, '--', color=aquifer_color, label=f'Theil-Sen Trend (slope={slope:.2f})', zorder=5)
    ax.fill_between(Dates, lower_ci, upper_ci, alpha=0.3, color=aquifer_color, label='90% Bootstrap CI')


    #ax.invert_yaxis()
    ax.set_title(f'{aquifer_name} Aquifer Depth Analysis: {start_date}-{end_date}\nTheil-Sen Trend with 90% Bootstrap CI', pad=20)
    ax.set_xlabel('Date')
    ax.set_ylabel('Depth (ft)')
    ax.grid(alpha=0.2)
    ax.legend(loc='upper right')

    plt.tight_layout()


    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        filename = f"{aquifer_name.replace(' ', '_').replace('(', '').replace(')', '').replace('-', 'v2')}.pdf"
        save_path = os.path.join(output_folder, filename)
        plt.savefig(save_path, dpi=300)
        print(f"Saved plot to: {save_path}")
    plt.close()
#"""
analyze_aquifer_data(file_path=aquifers['Pecos Valley']['path'], 
                    aquifer_name = 'Pecos Valley', start_date = 1920, end_date = 2020, 
                    output_folder = '/Users/finleydavis/Desktop')
"""
# Run the function for all aquifers
output_folder = '/Users/finleydavis/Desktop/Cardenas Research/Graph_pngs/Final Graphs/Confidence Interval'

for aquifer_name in aquifers:
    print(f"Processing {aquifer_name}...")
    analyze_aquifer_data(
        file_path=aquifers[aquifer_name]['path'],
        aquifer_name=aquifer_name,
        start_date=1920,
        end_date=2020,
        output_folder=output_folder
    )
"""