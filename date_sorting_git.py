import pandas as pd

# reads given aquifer csv file into a pandas dataframe
# Note: the number of columns varies per csv file, so the number of columns must be adjusted accordingly
csv_file = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala.csv'  
# variavble data now has my aquifer csv file loaded into it
data = pd.read_csv(csv_file)

"""
# this is the method to sort my data by date
data['Date'] = data.iloc[:, 12].apply(lambda x: x[-4:] if isinstance(x, str) and x[-4:].isdigit() else None)
# this is the method to sort my data by depth
"""
data.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
                'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16', 'Unnnamed17', 'Unnamed18']



# this sorts through the data and finds the Date,
# which is in the 12th column of the csv file
# the lambda function is used to apply the function to each element in the column
# in summary, this line of code creates a new column in the dataframe that contains the Date of the data

# removes rows that don't have any values in them
# this occurs in the csv file when there is a well depth, but no date, and makes up a good portion of the data
data = data.dropna(subset=['Date'])

# this does the same thing but for depth
data['Depth'] = pd.to_numeric(data['Depth'], errors='coerce')
data = data.dropna(subset=['Depth'])

# converts Date to integer using astype method
# returns new object with changed data type
data['Date'] = data['Date'].astype(int)

# replaces the original date with just 4 digit Date
# originally didn't do this, but it was causing issues with the sorting and errors in the data
# iloc is used to index the column
data.iloc[:, 12] = data['Date']

# drops the Date column if you don't want to keep it in the final output
data = data.drop(columns=['Date'])

# save the sorted CSV to a new file 
#data.to_csv('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/corrected/Ogallala1.csv', index=False)

# checking w/ print
print(data[['Date', 'Depth']].head())
