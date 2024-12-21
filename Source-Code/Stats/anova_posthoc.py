import pandas as pd
import os
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Define the directory paths
main_dir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
data_dir = os.path.join(main_dir, "Clean-Data")

file_names = [
    "clean-2020-data.csv",
    "clean-2021-data.csv",
    "clean-2022-data.csv",
    "clean-2023-data.csv"
]
years = [2020, 2021, 2022, 2023]
columns_for_anova = ["Annual Withdrawal Rate", "Annual Withdrawal Amount"]

# Function to drop rows with zero values
def drop_null_zero_rows(d: pd.DataFrame):
    return d[(d[['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income', 'Annual Withdrawal Rate', 'Annual Withdrawal Amount']] != 0).any(axis=1)].reset_index(drop=True)

# Read the data into dataframes and apply the drop function
dataframes = {year: drop_null_zero_rows(pd.read_csv(os.path.join(data_dir, file))) for year, file in zip(years, file_names)}

# Function to drop NaN values and check if there are enough values for the test
def drop_na_and_check(data):
    data = [d.dropna() for d in data]
    if all(len(d) > 1 for d in data):
        return data
    else:
        return None

# ANOVA Test
def perform_anova(dataframes, columns):
    print("ANOVA Results:")
    for column in columns:
        data = [dataframes[year][column] for year in years]
        data = drop_na_and_check(data)
        if data:
            _, p_value = f_oneway(*data)
            print(f"{column}: P-value = {p_value}")
        else:
            print(f"{column}: Not enough data for ANOVA")

# Perform ANOVA on the specified columns
perform_anova(dataframes, columns_for_anova)

# Post-hoc Test (Tukey's HSD)
def perform_post_hoc_test(dataframes, columns):
    print("\nPost-hoc Test Results:")
    for column in columns:
        melted_data = pd.concat([dataframes[year][[column]].assign(Year=year) for year in years])
        melted_data = melted_data.rename(columns={column: 'Value'}).dropna()
        if len(melted_data) > 1:
            posthoc = pairwise_tukeyhsd(melted_data['Value'], melted_data['Year'], alpha=0.05)
            print(f"\n{column}:\n", posthoc)
        else:
            print(f"{column}: Not enough data for post-hoc test")

# Perform post-hoc test on the specified columns
perform_post_hoc_test(dataframes, columns_for_anova)
