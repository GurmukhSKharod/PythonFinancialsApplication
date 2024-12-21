import pandas as pd
import pathlib
import numpy as np
import os

def get_data(parent):
    dir = pathlib.Path(parent/ 'Raw-Data')
    data = pd.read_csv(dir/'2020 FI Survey Results - LIGHTLY CLEANED DATA.csv', header=None)
    data = data.drop(index=0) 
    return data   

def del_columns(data: pd.DataFrame):
    columns_to_keep = np.array([2,11,21,27,33,52,53,54,55,56,
                       61,62,63,65,67,68,
                       70,71,74,77,80,83,84,85,86,
                       98,99])-1
    money_stat_cols = np.array(data.columns.get_indexer(['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income']))
    columns_to_keep = np.concatenate((columns_to_keep, money_stat_cols))
    data = data.iloc[:,columns_to_keep]
    return data

def set_column_names(data: pd.DataFrame):
    columns = ['Number of Contributors', 'Reside in US', 'Age', 'Relationship Status', 'Country',
                'Financially Independent', 'FI Number', 'Percent of FI Amount', 'Amount to Retire',
                'Target Safe Withdrawal Rate', 'Annual Income [Supplemental Sources]', 'Retired Annual Spending',
                'FI Number [Retired]', 'Retired', 'Intended Retirement Age', 'Work if FI', 'Annual Withdrawal Rate',
               'Annual Withdrawal Amount','Working Industry', 'Employer Type', 'Job Role','Full Time Employment', 
               'Part Time, Regular Employment', 'Part Time, Irregular Employement', 'Not Employed',
               'Housing Situation', 'Cost of Living Index',
               'Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income']
    assert(len(columns) == len(data.columns))
    data.columns = columns
    data['Year'] = 2020
    return data

def create_csv(parent_dir, data: pd.DataFrame):
    dir = pathlib.Path(parent_dir/'Clean-Data')
    os.makedirs(dir, exist_ok=True)
    data.to_csv(dir/'clean-2020-data.csv', index=False)

# merge age columns and relationship columns
def merge_data(data: pd.DataFrame):
    data[20] = data[20].fillna(data[39])
    data[26] = data[26].fillna(data[45])
    return data

def country_to_currency(data: pd.DataFrame):
    if data['Reside in US'] == 'Yes' or data['Country'].lower().strip() == 'us armed forces':
        return 'USD'
    if data['Country'].lower().strip() == 'canada':
        return "CAD"
    if data['Country'].lower().strip() in ['united kingdom', 'england']:
        return "GBP"
    if data['Country'].lower().strip() == 'australia':
        return "AUD"
    
    countries_using_euro = ['cyprus','estonia', 'finland', 'france', 'germany', 'ireland', 'italy',
                            'latvia', 'netherlands', 'the netherlands', 'portugal', 'slovakia', 
                            'slovenia', 'spain', 'eu', 'belgium', 'austria (eu)']
    if data['Country'].lower().strip() in countries_using_euro:
        return "EUR"
    
    # else
    return 'Other'

# sum data to obtain total assets, debt, income, expenses
def sum_money_stats(data: pd.DataFrame):
    data['Total Assets'] = data.iloc[:,99:107].fillna(0).map(float).sum(axis=1)
    data['Total Debt'] = data.iloc[:,107:114].fillna(0).map(float).sum(axis=1)
    data['Annual Expenses'] = data.iloc[:,115:128].fillna(0).map(float).sum(axis=1)
    data['Total Income'] = data.iloc[:,114]
    return data

# exchagne rates from the irs: https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates
def to_USD(data):
    currencies = ['USD','CAD', 'GBP','AUD','EUR']
    
    data = data[data['Currency Used'].isin(currencies)].copy()
    conversion = {'USD': 1,'CAD': 1.341, 'GBP': 0.779,'AUD': 1.452,'EUR':0.877}
    
    data['conversion'] = data['Currency Used'].map(conversion)
    cols = ['FI Number', 'Amount to Retire', 'Annual Income [Supplemental Sources]',
            'Retired Annual Spending', 'FI Number [Retired]', 'Annual Withdrawal Rate',
            'Total Assets','Total Debt','Annual Expenses','Total Income']
    data[cols] = data[cols].apply(pd.to_numeric)
    data[cols] = data[cols].div(data['conversion'], axis = 0)
    data = data.drop('conversion', axis =1)
    return data


def main():
    parent_dir = pathlib.Path(__file__).parents[2]
    data = get_data(parent_dir)
    data = merge_data(data)
    data = sum_money_stats(data)
    data = del_columns(data)
    data = set_column_names(data)
    currency_used = data.apply(country_to_currency, axis=1)
    data.insert(data.columns.get_loc('Country') + 1, 'Currency Used', currency_used)
    data = to_USD(data)
    create_csv(parent_dir,data)
    
if __name__ == '__main__':
    main()