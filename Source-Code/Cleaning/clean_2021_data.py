import numpy as np
import pandas as pd
import pathlib
import os

# Define the numerical indices of the columns to keep
columns_to_keep = [
    2, 11, 12, 22, 23, 25, 26, 39, 40, 41, 42, 43, 44, 45, 46, 
    65, 66, 67, 68, 69, 70, 71, 72, 77, 78, 79, 80, 81, 83, 85, 
    88, 89, 102, 110, 127, 132
]

# Define the new column names in the order corresponding to their indices
new_column_names = [
    'Number of Contributors', 'Reside in US', 'Currency Used', 
    'Age', 'Relationship Status', 'Children Currently', 'Children Desired', 
    'Full Time Employment', 'Part Time, Regular Employment', 
    'Part Time, Irregular Employement', 'Not Employed', 'Working Industry', 
    'Employer Type', 'Job Role', 'Job Title', 'Housing Situation', 
    'Cost of Living Index', 'Financially Independent', 'FI Number', 
    'Percent of FI Amount', 'Retired', 'Amount to Retire', 
    'Target Safe Withdrawal Rate', 'Annual Income [Supplemental Sources]', 
    'Retired Annual Spending', 'Type of FI', 'Work if FI', 
    'Intended Retirement Age', 'Inflation/Recession Effects', 'FI Number [Retired]', 
    'Annual Withdrawal Rate', 'Annual Withdrawal Amount', 'Total Assets', 
    'Total Debt', 'Annual Expenses', 'Total Income'
]

# reading the CSV file
def get_data(parent):
    dir = pathlib.Path(parent / 'Raw-Data')  # Path to the 'Raw-Data' directory
    data = pd.read_csv(dir / 'Reddit Financial Independence 2021 Survey.xlsx - Responses - CLEANED.csv')  # Read the CSV file
    return data

# remove unnecessary columns
def del_columns(data):
    # Select only the columns with the specified indices
    data = data.iloc[:, columns_to_keep]
    return data

# set new column names
def set_column_names(data):
    if len(data.columns) == len(new_column_names):
        data.columns = new_column_names  # Rename columns based on the new names
    else:
        raise ValueError("The number of new column names does not match the number of columns in the data.")
    data['Year'] = 2021  # Add a 'Year' column with the value 2021
    return data

# exchagne rates from the irs: https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates
def to_USD(data):
    currencies = ['USD','CAD', 'GBP','AUD','EUR']
    
    data = data[data['Currency Used'].isin(currencies)].copy()
    conversion = {'USD': 1,'CAD': 1.254, 'GBP': 0.727,'AUD': 1.332,'EUR':0.846}
    
    data['conversion'] = data['Currency Used'].map(conversion)
    cols = ['FI Number', 'Amount to Retire', 'Annual Income [Supplemental Sources]',
            'Retired Annual Spending', 'FI Number [Retired]', 'Annual Withdrawal Rate',
            'Total Assets','Total Debt','Annual Expenses','Total Income']
    data[cols] = data[cols].apply(pd.to_numeric)
    data[cols] = data[cols].div(data['conversion'], axis = 0)
    data = data.drop('conversion', axis =1)
    return data

# Function to save the cleaned data to a CSV file
def create_csv(parent_dir, data: pd.DataFrame):
    dir = pathlib.Path(parent_dir / 'Clean-Data')  # Path to the 'Clean-Data' directory
    os.makedirs(dir, exist_ok=True)  # Create the 'Clean-Data' directory if it doesn't exist
    data.to_csv(dir / 'clean-2021-data.csv', index=False)  # Save the cleaned data to a CSV file

# Main function
def main():
    parent_dir = pathlib.Path(__file__).parents[2]
    data = get_data(parent_dir)  # Read the CSV file
    data = del_columns(data)  # Remove unnecessary columns
    data = set_column_names(data)  # Set new column names
    data = to_USD(data)
    create_csv(parent_dir, data)  # Save the cleaned data to a CSV file

if __name__ == "__main__":
    main()
