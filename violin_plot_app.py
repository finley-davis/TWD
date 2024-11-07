
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


df = pd.read_csv('/Users/finleydavis/Desktop/Cardenas Research/Raw Data/Parsed Aquifers/Date Sorted/TWD Ogallala Excel CSV_parsed_datesorted.csv')

df.columns = ['Index', 'Unnamed1', 'Unnamed2', 'Unnamed3', 'Unnamed4', 'Unnamed5', 'Lat', 'Long',
              'Unnamed8', 'Unnamed9', 'Unnamed10', 'County', 'Date', 'Depth', 'Unnamed14', 'Unnamed15', 'Unnamed16', 'Unnamed17', 'Unnamed18']

#parsing and dropping data I don't need
df['Year'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce').dt.year
df = df.dropna(subset=['Year', 'Depth'])
df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')

#setting up bins and labels
minYear = int(df['Year'].min())
maxYear = int(df['Year'].max())
bins = list(range(minYear, maxYear + 1, 5))
labels = [f'{i}-{i+4}' for i in bins[:-1]]
df['Year_Bin'] = pd.cut(df['Year'], bins=bins, labels=labels, right=False)

#plot
def plot_violin(yearBin):
    filteredData = df[df['Year_Bin'] == yearBin]
    plt.figure(figsize=(10, 6))
    
    sns.violinplot(x='Year_Bin', y='Depth', data=filteredData, color='purple', inner='point')
    
    tickPosition = labels.index(yearBin)
    
    plt.xticks([tickPosition], [yearBin])  #

    plt.title(f'Violin Plot for {yearBin}')
    plt.xlabel('Year Bin')
    plt.ylabel('Depth')
    st.pyplot(plt) 

st.title("Interactive Violin Plot for 5-year Well Depth Data in the Ogallala Aquifer")

yearBin = st.selectbox("Select Interval:", labels)

if st.button("Refresh"):
    plot_violin(yearBin)



#streamlit run /Users/finleydavis/Desktop/Cardenas\ Research/Python/Graphs/violin_plot_app.py
