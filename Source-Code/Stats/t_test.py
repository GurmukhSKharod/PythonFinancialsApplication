import pandas as pd
import os
from scipy.stats import ttest_ind

# Define the directory paths
main_dir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
data_dir = os.path.join(main_dir, "Clean-Data")
output_dir = os.path.join(main_dir, "Stats-Results")

# Create the Results directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

file_names = [
    "clean-2020-data.csv",
    "clean-2021-data.csv",
    "clean-2022-data.csv",
    "clean-2023-data.csv"
]
years = [2020, 2021, 2022, 2023]
columns_to_analyze = ["Total Assets", "Total Debt", "Annual Expenses", "Total Income", "Annual Withdrawal Rate", "Annual Withdrawal Amount"]

# Function to drop rows with zero values
def drop_null_zero_rows(d: pd.DataFrame):
    return d[(d[['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income', 'Annual Withdrawal Rate', 'Annual Withdrawal Amount']] != 0).any(axis=1)].reset_index(drop=True)

# Read the data into dataframes and apply the drop function
dataframes = {year: drop_null_zero_rows(pd.read_csv(os.path.join(data_dir, file))) for year, file in zip(years, file_names)}

# Function to drop NaN values and check if there are enough values for the test
def drop_na_and_check(data1, data2):
    data1 = data1.dropna()
    data2 = data2.dropna()
    if len(data1) > 1 and len(data2) > 1:
        return data1, data2
    else:
        return None, None

# T-test and save results to a CSV file
def perform_t_test_and_save(dataframes, columns):
    results = []
    for column in columns:
        for i in range(len(years)):
            for j in range(i + 1, len(years)):
                data1, data2 = drop_na_and_check(dataframes[years[i]][column], dataframes[years[j]][column])
                if data1 is not None and data2 is not None:
                    _, p_value = ttest_ind(data1, data2)
                    results.append({
                        "Column": column,
                        "Year1": years[i],
                        "Year2": years[j],
                        "P-value": p_value
                    })
                else:
                    results.append({
                        "Column": column,
                        "Year1": years[i],
                        "Year2": years[j],
                        "P-value": "N/A"
                    })

    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(output_dir, "t_test_results.csv"), index=False)
    print(f"T-test results saved to {os.path.join(output_dir, 't_test_results.csv')}")

# Perform T-test on all possible combinations of years and save results
perform_t_test_and_save(dataframes, columns_to_analyze)
