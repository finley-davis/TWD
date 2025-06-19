#importing libraries
#pandas is a data manipulation library
import pandas as pd
#numpy is a numerical computation library
import numpy as np
#scipy is a scientific computation library, for lognormal distribution
from scipy.stats import lognorm
#matplotlib is a plotting library
import matplotlib.pyplot as plt

#set the start and end year for the data
start_year = 1920
end_year = 2025

#file path for the csv file

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
#read the csv file into a pandas dataframe

df = pd.read_csv(aquifers['Ogallala']['path'])

#renaming the columns of the dataframe
df.columns = ['Index', 'Lat', 'Long','County', 'Date', 'Depth']

#convert the date column to datetime format, datetime is a data type that can be manipulated as dates
df['Date'] = pd.to_datetime(df['Date'], format='%Y', errors='coerce')

#filter the dataframe to include only rows within the specified date range, using the start_year and end_year variables
df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]

#taking the year from the date column in the csv file and creating a new year column
df['Year'] = df['Date'].dt.year

#converting the depth column to numeric, coercing errors to NaN
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
#drop rows with NaN values in the depth column, this is just a check to make sure there are no NaN values
df = df.dropna(subset=['Depth'])

#creating bins for every 5 years within the date range, you can change the interval by changing the 5 to a different number
bins = list(range(start_year, end_year + 1, 5))
#creating labels for the bins
labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins) - 2)]
# Handle the last label to end at the last year in the data
last_bin_start = bins[-2]
last_year = df['Year'].max()
labels.append(f'{last_bin_start}-{last_year}')

#bin the year column into the created bins and create a new Year_Bin column
df['Year_Bin'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)

#set the figure size for the plot, this is the size of the plot in inches, typically 12 x 6 but in this case 15 x 10 because of the size of the data
plt.figure(figsize=(15, 10))

#getting the unique year bins and sort them
year_bins = sorted([bin for bin in df['Year_Bin'].unique() if not pd.isna(bin)])
#creating an array of positions for the x-axis
x_positions = np.arange(len(year_bins))

#getting the maximum and minimum depth values
max_depth = df['Depth'].max()
min_depth = df['Depth'].min()
#creating bin edges for the depth histogram
bin_edges = np.linspace(min_depth, max_depth, 50)  
#calculating the midpoints of the bin edges, which will be used for plotting the lognormal distribution
y_points = (bin_edges[:-1] + bin_edges[1:]) / 2 

#iterating over each year bin
for i, year_bin in enumerate(year_bins):
    #subset the dataframe for the current year bin
    #this is a subset of the dataframe that only includes the rows where the Year_Bin column is equal to the current year bin
    subset = df[df['Year_Bin'] == year_bin]
    #get the depth values for the subset
    #this is an array of the depth values for the current year bin
    #for log-normal dist.
    depth_data = subset['Depth'].values

    #creating a histogram plot of the depth values
    hist, _ = np.histogram(subset['Depth'], bins=bin_edges, density=True)

    #scaling histogram vlaues between 1 and 0 (normalizing)
    hist = hist / hist.max() * 0.4 
    
    #plot the histogram as horizontal bars on the left side
    #this is how i'm making the hist plot horizontal (up and down) instead of vertical (left and right)
    plt.barh(bin_edges[:-1], -hist, height=np.diff(bin_edges), 
             left=i, color='red', label = 'Histogram' if i == 0 else "")

    #plot the histogram as horizontal bars on the right side
    #height = is the height of the bars based on the bin edges, which are the depth values
    plt.barh(bin_edges[:-1], hist, height=np.diff(bin_edges), 
             left=i, color='red')

    #depth data points, data for log norm. dist.
    if len(depth_data) > 0: 
        #calculating the log of the depth data
        log_depth = np.log(depth_data)
        #calculating the mean and standard deviation of the log depth data
        mu, sigma = log_depth.mean(), log_depth.std()
        
        #calculate the lognormal probability density function
        pdf = lognorm.pdf(y_points, s=sigma, scale=np.exp(mu))

        #normalize the pdf values
        pdf = pdf / pdf.max() * 0.4
        #print(pdf)

        #plot the pdf on the left side
        plt.plot(i - pdf, y_points, 'black', linewidth=2, label='Lognormal PDF' if i == 0 else "")
        #plot the pdf on the right side
        plt.plot(i + pdf, y_points, 'black', linewidth=2)

        #mean values in normal space
        mean_original = np.exp(mu + 0.5 * sigma**2)
        #standard deviation in normal space
        std_original = np.sqrt((np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2))


        #mean depth annotation
        mu_annotation = f'μ = {mean_original:.2f}'
        sigma_annotation = f'σ = {std_original:.2f}'
        #plt.text(i, min_depth - 30, mu_annotation, ha='center', fontsize=7.5, color='blue')
        #plt.text(i, min_depth - 16, sigma_annotation, ha='center', fontsize=7.5, color='purple')
        #export the mean and std to a csv file
        #this is just printing the mean and standard deviation for each year bin
        print(f'{year_bin}, {mean_original:.2f}, {std_original:.2f}')
        #export to csv file
        with open('lognormal_params.csv', 'a') as f:
            f.write(f'{year_bin}, {mean_original:.2f}, {std_original:.2f}\n')

        
        #i've kept this in from the original code histogram plot code (which is one graph for a 5 year period)
        #but it's not necessary and makes the graph look weird
        """
        #add mean depth line
        mean_depth = np.exp(mu)
        plt.axhline(y=mean_depth, xmin=(i-0.4)/len(year_bins), 
               xmax=(i+0.4)/len(year_bins), 
               color='g', linestyle='--', linewidth=2)
        """

#theil-sen line
#calculating the median of the depth data
median_depth = df['Depth'].median()
lognorm_median = np.exp(df['Depth'].apply(np.log).median())
#plotting the median depth line
#plt.axhline(y=median_depth, color='b', linestyle='--', linewidth=2, label='Median Depth')


#setting title of the plot
plt.title('Ogallala Aquifer Depth Distribution with Lognormal Fit (1920-2023)', pad=20)
#setting x-axis label
plt.xlabel('Year Interval')
#setting y-axis label
plt.ylabel('Depth (ft)')

#setting x-axis ticks, which are the year bins
plt.xticks(x_positions, year_bins, rotation=45, ha='right')

#flip y-axis
plt.gca().invert_yaxis()
#adding a grid to the y-axis, which is the depth axis
plt.grid(True, axis='y', linestyle='--')

#adding a legend
#plt.plot([], [], 'r', linewidth=2, label='Lognormal PD#F')

#plot the legend in bottom right corner
plt.legend(loc='upper right', fontsize=12)

#adjusting the layout to fit everything
plt.tight_layout()

#displaying the plot
#plt.show()
