import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm

def lognormal_mean(x):
    x = x[x > 0].dropna()  # Remove non-positive and NaN values
    if len(x) == 0:
        return np.nan
    elif len(x) == 1:
        return x.iloc[0]
    log_x = np.log(x)
    return np.exp(log_x.mean() + 0.5 * log_x.std() ** 2)


def plot_9aquifer_water_levels():
    # Load your CSV
    df = pd.read_csv('/Users/finleydavis/Desktop/Cardenas Research/Python/aquifer_water_levels.csv')

    # List of unique aquifers
    aquifers = df['Aquifer'].unique()

    # Create a figure with 9 subplots (3 rows, 3 columns)
    fig, axes = plt.subplots(3, 3, figsize=(15, 10))
    axes = axes.flatten()

    # Loop through each aquifer and plot its data
    for i, aquifer in enumerate(aquifers):
        aquifer_df = df[df['Aquifer'] == aquifer]

        # Compute log-normal mean depth per year
        yearly_lognorm = (
            aquifer_df.groupby('Year')['WaterLevel']
            .apply(lognormal_mean)
            .reset_index(name='LognormMean')
        )

        # Drop NaN log-normal means before regression
        yearly_lognorm = yearly_lognorm.dropna(subset=['LognormMean'])

        if len(yearly_lognorm) < 2:
            continue  # Not enough data to fit a line

        # Perform linear regression
        X = yearly_lognorm['Year'].values.reshape(-1, 1)
        y = yearly_lognorm['LognormMean'].values
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        slope = model.coef_[0]

        # Plot the log-normal means
        axes[i].scatter(yearly_lognorm['Year'], yearly_lognorm['LognormMean'],
                        marker='o', color='teal', label='Log-normal Mean')

        # Plot the regression line
        axes[i].plot(yearly_lognorm['Year'], y_pred, color='red', linestyle='--', label='Linear Fit')

        # Add slope text annotation to the plot
        slope_text = f"Slope: {slope:.2f} ft/yr"
        axes[i].text(0.05, 0.95, slope_text, transform=axes[i].transAxes,
                     fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))

        # Customize subplot
        axes[i].set_title(f'{aquifer} Aquifer Log-normal Water Levels', fontsize=11)
        axes[i].set_xlabel('Year')
        axes[i].set_ylabel('Water Level (ft AMSL)')
        axes[i].grid(True)
        axes[i].legend()

    plt.tight_layout()
    plt.show()

def count_values_per_aquifer():
    df = pd.read_csv('/Users/finleydavis/Desktop/Cardenas Research/Python/aquifer_water_levels.csv')
    aquifers = df['Aquifer'].unique()
    counts = {}

    for aquifer in aquifers:
        aquifer_df = df[df['Aquifer'] == aquifer]

        # Count how many valid water levels (positive and non-null) per year
        valid_counts_per_year = (
            aquifer_df[ aquifer_df['WaterLevel'] > 0 ]
            .groupby('Year')['WaterLevel']
            .count()
        )

        # Sum counts across all years to get total values used
        total_values = valid_counts_per_year.sum()
        counts[aquifer] = total_values
    print(counts)
    return counts

#plot_9aquifer_water_levels()
#count_values_per_aquifer()

