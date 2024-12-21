import pandas as pd
import numpy as np
import pathlib
import matplotlib.pyplot as plt
from scipy.stats import linregress

#Gurmukh wrote this
# Alternative function to drop rows with zero values
def drop_zeros(d: pd.DataFrame):
    return d[(d[['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income', 'Annual Withdrawal Rate', 'Annual Withdrawal Amount']] != 0).any(axis=1)].reset_index(drop=True)

#returns the dataframe with the mean of the columns we are examining
def get_means(data):
    data['Total Assets'] = data['Total Assets'].mean()
    data['Total Debt'] = data['Total Debt'].mean()
    data['Annual Expenses'] = data['Annual Expenses'].mean()
    data['Total Income'] = data['Total Income'].mean()
    data['Annual Withdrawal Rate'] = data['Annual Withdrawal Rate'].mean()
    data['Annual Withdrawal Amount'] = data['Annual Withdrawal Amount'].mean()
    return data.iloc[0]


#get the yearly information related to totals with zeros dropped
def get_columns(dir):
    cols = ['Total Assets','Total Debt','Annual Expenses','Total Income', 'Annual Withdrawal Rate', 'Annual Withdrawal Amount']
    d2020 = pd.read_csv(dir/'clean-2020-data.csv',usecols=cols)
    d2020 = get_means(d2020)
    d2020['year'] = 2020

    d2021 = pd.read_csv(dir/'clean-2021-data.csv',usecols=cols)
    d2021 = get_means(d2021)
    d2021['year'] = 2021

    d2022 = pd.read_csv(dir/'clean-2022-data.csv',usecols=cols)
    d2022 = get_means(d2022)
    d2022['year'] = 2022

    d2023 = pd.read_csv(dir/'clean-2023-data.csv',usecols=cols)
    d2023 = get_means(d2023)
    d2023['year'] = 2023
    
    return pd.concat([d2020,d2021,d2022,d2023],axis = 1).transpose().reset_index(drop=True)

# https://ourworldindata.org/grapher/global-gdp-over-the-long-run
def get_gdp(dir):
    data = pd.read_csv(dir / 'global gdp.csv', header=0)
    data = data.drop(['Entity', 'Code'], axis = 1)
    data = data[data['Year']> 2019]
    #data['Year'] = pd.to_datetime(data['Year'])
    return data

#from: https://ca.finance.yahoo.com/quote/%5ESP500TR/
def get_sp(dir):
    data = pd.read_csv(dir / 'SP500TR.csv', header=0)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    groups = data.groupby(data['Year'])
    data = groups.aggregate({'Open': 'mean'})
    data.reset_index(inplace=True)
    return data

# https://www.macrotrends.net/2015/fed-funds-rate-historical-chart
def get_interest_rates(dir):
    data = pd.read_csv(dir / 'interest rates.csv', header=0)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data = data[data['Year']>2019]
    data = data[data['Year']<2024]

    
    data.dropna(inplace=True)
    groups = data.groupby(data['Year'])
    
    data = groups.aggregate({'Value': 'mean'})
    data.reset_index(inplace=True)

    return data

    
def plots(graph_dir, gdp, sp,  iRates):
    plt.subplot(2,2,1)
    plt.plot(gdp['Year'], gdp['GDP'], marker = 'o')
    plt.xticks(gdp['Year'])  # Set x-ticks to the years
    plt.ylabel('US dollars')
    plt.xlabel('Year')

    plt.title('Global GDP by Year')

    plt.subplot(2,2,2)
    plt.plot(sp['Year'], sp['Open'], marker = 'o')
    plt.ylabel('Points')
    plt.xlabel('Year')
    plt.xticks(sp['Year'])  # Set x-ticks to the years
    plt.title('Average S&P 500 total return')

    plt.subplot(2,2,3)
    plt.plot(iRates['Year'], iRates['Value'], marker = 'o')
    plt.ylabel('US Interest Rate (%)')
    plt.xlabel('Year')
    plt.xticks(iRates['Year'])  # Set x-ticks to the years
    plt.title('USA Federal Funds (Interest) Rate')

    plt.tight_layout()

    plt.savefig(graph_dir/'world factors')

#check the linear correlation between our world metrics and FI Data
def do_correlation(FI_data, gdp, sp, iRates):
    columns = FI_data.columns
    for col in columns:
        if col != 'year':
            print(col+ ' and S&P500 Correlation Coefficient' + str(linregress(sp['Open'],FI_data[col]).rvalue))
            print(col+ ' and Interest Rates Correlation Coefficient' + str(linregress(iRates['Value'],FI_data[col]).rvalue))
    dropped2022 = FI_data.drop(3)
    for col in columns:
        if col != 'year':
            print(col+ ' and Global GDP Correlation Coefficient' + str(linregress(gdp['GDP'],dropped2022[col]).rvalue))
    

def main():
    parent_dir = pathlib.Path(__file__).parents[2]
    dir = pathlib.Path(parent_dir / 'Raw-Data')  # Path to the 'Raw-Data' directory
    cleandir = pathlib.Path(parent_dir / 'Clean-Data')  # Path to the 'Raw-Data' directory
    graph_dir = pathlib.Path(parent_dir / 'graphs')
    #get yearly global GDP
    gdp = get_gdp(dir)
    #get yearly S&P500TR
    sp = get_sp(dir)
    #get interest rates
    iRates = get_interest_rates(dir)
    #get the yealry data to comapre
    data = get_columns(cleandir)
    plots(graph_dir, gdp, sp, iRates)
    do_correlation(data, gdp, sp, iRates)


if __name__ == '__main__':
    main()