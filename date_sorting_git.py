import pandas as pd

# reads given aquifer csv file into a pandas dataframe
# Note: the number of columns varies per csv file, so the number of columns must be adjusted accordingly
csv_file = '/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/Edwards (Balcones Fault Zone) Aquifer.csv'  
# variavble data now has my aquifer csv file loaded into it
data = pd.read_csv(csv_file)

# this is the method to sort my data by date
data['Year'] = data.iloc[:, 12].apply(lambda x: x[-4:] if isinstance(x, str) and x[-4:].isdigit() else None)
# this sorts through the data and finds the year, which is in the 12th column of the csv file
# the lambda function is used to apply the function to each element in the column
# in summary, this line of code creates a new column in the dataframe that contains the year of the data


# removes rows that don't have any values in them
# this occurs in the csv file when there is a well depth, but no date, and makes up a good portion of the data
data = data.dropna(subset=['Year'])

# converts year to integer using astype method
# returns new object with changed data type
data['Year'] = data['Year'].astype(int)

#replaces the orginal date with just 4 digit year
# originally didn't do this, but it was causing issues with the sorting and errors in the data
# iloc is used to index the column
data.iloc[:, 12] = data['Year']

# drops the year column if you don't want to keep it in the final output
data = data.drop(columns=['Year'])

# save the sorted CSV to a new file 
data.to_csv('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/Edwards (Balcones Fault Zone) Aquifer.csv', index=False)

# checking w/ print
print(data.head())
