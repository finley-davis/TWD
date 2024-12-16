import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#year range, this can be changed based on what years you want to look at
#this is meant to be a 5 year interval
start_year = 2005
end_year = 2020

#loading in CSV file
file_path = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'
#read file path to data variable
data = pd.read_csv(file_path)

#rename columns based on CSV file, may have to change based on CSV file
data.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16', 'Unnamed17', 'Unnamed18']

#convert date column to datetime object
data['Date'] = pd.to_datetime(data['Date'], format='%Y', errors='coerce')

#drops rows with no date or depth (just a reassurance that there are no errors in the pre-filtered data)
data = data.dropna(subset=['Date', 'Depth'])
#converts date to year (just want 4 digits)
data['Year'] = data['Date'].dt.year
#filters data to only include years between start_year and end_year that was defined at the top
data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

#violin plot function for well depth in relation to time
def plot_violin(start_year, end_year):
    #creates 5-year seperation
    bins = list(range(start_year, end_year + 1, 5))
    labels = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins) - 1)]
    #creates a new column in the dataframe that contains the year interval
    data['Year_Bin'] = pd.cut(data['Year'], bins=bins, labels=labels, right=False)

    #plot violin plot for each bin
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='Year_Bin', y='Depth', data=data, palette='muted') #inner='point')
    sns.stripplot(x='Year_Bin', y='Depth', data=data, color='black', size=3, jitter=True, alpha=0.7)

    #labeling the graph
    plt.title(f'Ogallala Violin Plots for 5-Year Intervals ({start_year}-{end_year})')
    plt.xlabel('Year Interval')
    plt.ylabel('Depth')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#running the function
if __name__ == "__main__":
   plot_violin(start_year, end_year)