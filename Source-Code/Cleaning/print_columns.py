import pandas as pd
import pathlib

def col_index_to_letter(index):
    index += 1  # Excel columns are 1-based, not 0-based
    letters = []
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters.append(chr(65 + remainder))
    return ''.join(reversed(letters))

def print_all_column_names(filepath):
    # Read the CSV file
    data = pd.read_csv(filepath, header=0)  # Adjust header parameter if necessary
    
    # Set pandas options to display all columns
    pd.set_option('display.max_columns', None)  # Show all columns in the output
    pd.set_option('display.max_colwidth', None)  # Show full column names without truncation

    # Print all column names with corresponding letters and indices
    print("Column names in the CSV file with their corresponding letters and numbers:")
    for i, col in enumerate(data.columns):
        letter = col_index_to_letter(i)
        print(f"Column {i}: {letter} ({i}): {col}")

    # Print the total number of columns
    total_cols = len(data.columns)
    print(f"\nTotal number of columns: {total_cols}")

def main():
    # Determine the parent directory
    parent_dir = pathlib.Path(__file__).parents[0]
    
    # Specify the path to your CSV files in Clean-Data or Raw-Data
    clean_data_path = parent_dir / 'Clean-Data' / 'clean-2021-data.csv'
    raw_data_path = parent_dir / 'Raw-Data' / 'Reddit Financial Independence 2021 Survey.xlsx - Responses - CLEANED.csv'

    # Print the column names with letters, numbers, and the total number of columns
    print("Clean Data Columns: \n")
    print_all_column_names(clean_data_path)
    print("\n\n\nRaw Data Columns: ")
    print_all_column_names(raw_data_path)


if __name__ == "__main__":
    main()
