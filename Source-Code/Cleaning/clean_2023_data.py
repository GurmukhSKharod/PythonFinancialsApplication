import numpy as np
import pandas as pd
import pathlib
import os


def get_data(parent):
    dir = pathlib.Path(parent/ 'Raw-Data')
    data = pd.read_csv(dir/'Reddit Financial Independence 2023 Survey - CLEAN.xlsx - Responses.csv', header=None)
    data = data.drop(index=0) 
    return data   

def to_letter(val):
    if val<26:
        return chr(val+65)
    c = [chr((val//26)+64), chr(val%26+65)]
    return ''.join(c)

def del_columns(data):
    vec = np.vectorize(to_letter)
    keep = ['C', 'D', 'E', 'I', 'J', "L", 'M', 'X' ,'Y', 'Z', 'AA', 
            'AB', 'AC', 'AD', 'AE', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG','BH', 'BI', 
            'BN', 'BO', 'BP', 'BQ', 'BR', 'BT', 'BX', 'CA', 'CB', 'CO',
              'CW', 'DN', 'DU']
    data.columns = vec(data.columns)
    data = data[keep]
    return data

def set_column_names(data):
    cols = ['Number of Contributors', 'Reside in US', 'Currency Used', 'Age', 'Relationship Status',
               'Children Currently', 'Children Desired', 
               'Full Time Employment', 'Part Time, Regular Employment', 'Part Time, Irregular Employement','Not Employed',
               'Working Industry', 'Employer Type', 'Job Role', 'Job Title',
                'Housing Situation', 'Cost of Living Index', 'Financially Independent',
               'FI Number', 'Percent of FI Amount', 'Retired', 'Amount to Retire',

               'Target Safe Withdrawal Rate', 'Annual Income [Supplemental Sources]', 'Retired Annual Spending',
               'Type of FI','Work if FI', 'Intended Retirement Age', 'Inflation/Recession Effects', 'FI Number [Retired]', 'Annual Withdrawal Rate',
               'Annual Withdrawal Amount', 'Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income']
    data.columns = cols
    data['Year'] = 2023
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
                  'Canadian Dollars (CAD)': 1.350, 
                  'British Pound Sterling (GBP)': 0.804,
                  'Australian Dollars (AUD)': 1.506,
                  'Euros (EUR)':0.924
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
    data.to_csv(dir/'clean-2023-data.csv', index=False)


def main():
    parent_dir = pathlib.Path(__file__).parents[2]
    data =get_data(parent_dir)
    data = del_columns(data)
    data = set_column_names(data)
    data = to_USD(data)
    create_csv(parent_dir, data)


if __name__ == "__main__":
    main()
