import pandas as pd
import pathlib
import numpy as np
import os

def get_data(parent):
    dir = pathlib.Path(parent/ 'Raw-Data')
    data = pd.read_csv(dir/'Reddit Financial Independence 2022 Survey - Clean.xlsx - Responses.csv', header=None)
    data = data.drop(index=0) 
    return data   

def del_columns(data: pd.DataFrame):
    columns_to_del = np.array(np.arange(4,7).tolist()+[9]+np.arange(12,20).tolist()+np.arange(28,50).tolist()+
                      np.arange(58,62).tolist()+[64,67,68,69,71,72]+np.arange(75,87).tolist()+np.arange(88,95).tolist()+
                      np.arange(96,112).tolist()+[113,114,115,116,118])-1
    data = data.drop(columns=columns_to_del)
    return data

def set_column_names(data: pd.DataFrame):
    columns = ['Number of Contributors', 'Reside in US', 'Currency Used', 'Age', 'Relationship Status',
               'Children Currently', 'Children Desired', 'Working Industry', 'Employer Type', 'Job Role', 'Job Title',
               'Full Time Employment', 'Part Time, Regular Employment', 'Part Time, Irregular Employement',
               'Not Employed', 'Housing Situation', 'Cost of Living Index', 'Financially Independent',
               'FI Number', 'Percent of FI Amount', 'Retired', 'Amount to Retire',
               'Target Safe Withdrawal Rate', 'Annual Income [Supplemental Sources]', 'Retired Annual Spending',
               'Work if FI', 'Intended Retirement Age', 'FI Number [Retired]', 'Annual Withdrawal Rate',
               'Annual Withdrawal Amount', 'Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income']
    data.columns = columns
    data['Year'] = 2022
    return data

# exchagne rates from the irs: https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates
def to_USD(data):
    currencies = ['United States Dollars (USD)', 
                  'Canadian Dollars (CAD)', 
                  'British Pound Sterling (GBP)',
                  'Australian Dollars (AUD)',
                  'Euros (EUR)']
    
    data = data[data['Currency Used'].isin(currencies)].copy()
    conversion = {'United States Dollars (USD)': 1, 
                  'Canadian Dollars (CAD)': 1.301, 
                  'British Pound Sterling (GBP)': 0.811,
                  'Australian Dollars (AUD)': 1.442,
                  'Euros (EUR)':0.951
                  }
    
    data['conversion'] = data['Currency Used'].map(conversion)
    cols = ['FI Number', 'Amount to Retire', 'Annual Income [Supplemental Sources]',
            'Retired Annual Spending', 'FI Number [Retired]', 'Annual Withdrawal Rate',
            'Total Assets','Total Debt','Annual Expenses','Total Income']
    data[cols] = data[cols].apply(pd.to_numeric)
    data[cols] = data[cols].div(data['conversion'], axis = 0)
    data = data.drop('conversion', axis =1)
    return data

def create_csv(parent_dir, data: pd.DataFrame):
    dir = pathlib.Path(parent_dir/'Clean-Data')
    os.makedirs(dir, exist_ok=True)
    data.to_csv(dir/'clean-2022-data.csv', index=False)

def main():
    parent_dir = pathlib.Path(__file__).parents[2]
    data = get_data(parent_dir)
    data = del_columns(data)
    data = set_column_names(data)
    data = to_USD(data)
    create_csv(parent_dir,data)
    
if __name__ == '__main__':
    main()