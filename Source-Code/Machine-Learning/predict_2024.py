import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline

# Define the directory paths
main_dir = os.path.abspath(os.path.join(os.getcwd(), '../..'))
data_dir = os.path.join(main_dir, "Clean-Data")
graphs_dir = os.path.join(main_dir, "Graphs")
stats_results_dir = os.path.join(main_dir, "Stats-Results")  # Path to the stats results

# Create the Graphs directory if it doesn't exist
os.makedirs(graphs_dir, exist_ok=True)

file_names = [
    "clean-2020-data.csv",
    "clean-2021-data.csv",
    "clean-2022-data.csv",
    "clean-2023-data.csv"
]
years = [2020, 2021, 2022, 2023]
columns_to_predict = ["Total Assets", "Total Debt", "Annual Expenses", "Total Income"]

# Add 2024 to the years array
years_extended = years + [2024]
X_extended = np.array(years_extended).reshape(-1, 1)
predictions = {}

# Load the t-test results
t_test_results_file = os.path.join(stats_results_dir, "t_test_results.csv")
t_test_results_df = pd.read_csv(t_test_results_file)

# Load the data into dataframes and apply the drop function
def drop_zeros(d: pd.DataFrame):
    return d[(d[['Total Assets', 'Total Debt', 'Annual Expenses', 'Total Income']] != 0).any(axis=1)].reset_index(drop=True)

dataframes = {year: drop_zeros(pd.read_csv(os.path.join(data_dir, file))) for year, file in zip(years, file_names)}

# Function to get significant years from t-test results
def get_significant_years(t_test_results_df):
    significant_years = set()
    for _, row in t_test_results_df.iterrows():
        if row["P-value"] < 0.05:
            significant_years.add(row["Year1"])
            significant_years.add(row["Year2"])
    return sorted(significant_years)

# Get significant years from t-test results
significant_years = get_significant_years(t_test_results_df)

# Filter dataframes to include only significant years
dataframes_significant = {year: df for year, df in dataframes.items() if year in significant_years}
years_significant = sorted(significant_years)

# Train and predict using both Linear and Polynomial Regression
def train_and_predict(column_name):
    # Collect all data points for the given column
    y_all = np.concatenate([dataframes_significant[year][column_name].dropna().values for year in years_significant])
    X_all = np.concatenate([np.full_like(dataframes_significant[year][column_name].dropna().values, year) for year in years_significant])
    
    # Linear Regression
    linear_model = LinearRegression()
    linear_model.fit(X_all.reshape(-1, 1), y_all)
    y_pred_linear = linear_model.predict(X_extended)
    
    # Polynomial Regression
    polynomial_features = PolynomialFeatures(degree=2)  # Degree 2 polynomial
    polynomial_model = make_pipeline(polynomial_features, LinearRegression())
    polynomial_model.fit(X_all.reshape(-1, 1), y_all)
    y_pred_poly = polynomial_model.predict(X_extended)
    
    predictions[column_name] = {
        "linear": y_pred_linear,
        "polynomial": y_pred_poly
    }
    
    mse_linear = mean_squared_error(y_all, linear_model.predict(X_all.reshape(-1, 1)))
    r2_linear = r2_score(y_all, linear_model.predict(X_all.reshape(-1, 1)))
    
    mse_poly = mean_squared_error(y_all, polynomial_model.predict(X_all.reshape(-1, 1)))
    r2_poly = r2_score(y_all, polynomial_model.predict(X_all.reshape(-1, 1)))
    
    print(f"{column_name} - Linear Regression: MSE = {mse_linear}, R^2 = {r2_linear}")
    print(f"{column_name} - Polynomial Regression: MSE = {mse_poly}, R^2 = {r2_poly}")

# Train and predict for each column
for column in columns_to_predict:
    train_and_predict(column)

# Function to create and save a prediction graph
def create_prediction_graph(column_name, years, actual_means, predicted_values, years_extended, y_label):
    plt.figure(figsize=(12, 8))
    
    # Plot actual values (means) for the years
    plt.plot(years, actual_means, marker='o', linestyle='-', label=f'Actual {column_name}')
    
    # Plot linear regression
    plt.plot(years_extended, predicted_values["linear"], marker='x', linestyle='--', label='Linear Regression')
    
    # Plot polynomial regression
    plt.plot(years_extended, predicted_values["polynomial"], marker='^', linestyle='--', label='Polynomial Regression')
    
    plt.xlabel('Year')
    plt.ylabel(y_label)
    plt.title(f'{column_name} Prediction')
    plt.xticks(years_extended)  # Set x-ticks to the years
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graphs_dir, f'{column_name.replace(" ", "_").lower()}_prediction_comparison.png'))
    plt.show()

# Create and save prediction graphs for each column
for column in columns_to_predict:
    actual_means = [dataframes_significant[year][column].mean() for year in years_significant]
    predicted_values = predictions[column]
    y_label = 'Values ($)' if column != "Annual Withdrawal Rate" else 'Percentage (%)'
    create_prediction_graph(column, years_significant, actual_means, predicted_values, years_extended, y_label)
