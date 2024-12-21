import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the directory paths
main_dir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
data_dir = os.path.join(main_dir, "Clean-Data")
graphs_dir = os.path.join(main_dir, "Graphs")

# Create the Graphs directory if it doesn't exist
os.makedirs(graphs_dir, exist_ok=True)

file_names = [
    "clean-2020-data.csv",
    "clean-2021-data.csv",
    "clean-2022-data.csv",
    "clean-2023-data.csv"
]
years = [2020, 2021, 2022, 2023]
columns_to_graph = [
    "Annual Withdrawal Rate", "Annual Withdrawal Amount",
    "Total Assets", "Total Debt", "Annual Expenses", "Total Income"
]

# Alternative function to drop rows with zero values
def drop_zeros(d: pd.DataFrame):
    return d[(d[['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income', 'Annual Withdrawal Rate', 'Annual Withdrawal Amount']] != 0).any(axis=1)].reset_index(drop=True)

# Read the data into dataframes and apply the drop function
dataframes = {year: drop_zeros(pd.read_csv(os.path.join(data_dir, file))) for year, file in zip(years, file_names)}

# Calculate the mean values for each column and year
mean_values = {column: [dataframes[year][column].mean() for year in years] for column in columns_to_graph}

# Function to create and save a graph
def create_graph(column_name, mean_values, years, y_label):
    plt.figure(figsize=(10, 6))
    plt.plot(years, mean_values, marker='o', linestyle='-', label=column_name)
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.title(f'Average {column_name}')
    plt.xticks(years)  # Set x-ticks to the years
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graphs_dir, f'{column_name.replace(" ", "_").lower()}_average.png'))
    plt.show()

# Create and save graphs for each column
for column in columns_to_graph:
    y_label = 'Values ($)' if column != "Annual Withdrawal Rate" else 'Percentage (%)'
    create_graph(column, mean_values[column], years, y_label)

# Function to create and save a combined graph
def create_combined_graph(columns, mean_values, years):
    plt.figure(figsize=(12, 8))
    for column in columns:
        plt.plot(years, mean_values[column], marker='o', linestyle='-', label=column)
    plt.xlabel('Year')
    plt.ylabel('Values')
    plt.title('Average Values Comparison')
    plt.xticks(years)  # Set x-ticks to the years
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graphs_dir, 'combined_average_values.png'))
    plt.show()

# Create and save the combined graph for selected columns
columns_to_combine = ["Annual Withdrawal Amount", "Total Debt", "Annual Expenses", "Total Income"]
create_combined_graph(columns_to_combine, mean_values, years)
