# PythonFinancialsApplication Overview
The following Python Machine Learning and Stats App uses Numpy and Pandas.

It manipulates data from several csv files, to determine trends in different financial statistics over the course of several years. 

Stats fundamentals were used to see the changes in data, and Machine Learning fundamentals such as linear/polynomial regression was used to predict future data.

## External Libraries and Technologies Used
* Python
* Jupyter Notebook
* Pandas
* NumPy
* Matplotlib
* SciPy
* Scikit-learn

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=Pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=NumPy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C.svg?style=for-the-badge&logo=&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style=for-the-badge&logo=SciPy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

## Order of Execution and Expected Outputs
1. Navigate to the Source-Code/Cleaning directory and run all 4 data cleaning scripts in the directory. As an example, to run clean_2020_data.py, execute the command: _python3 clean_2020_data.py_. Once complete, inside the Clean-Data directory, there should be 4 clean versions of the raw data sets found in the Raw-Data directory.
2. Navigate to the Source-Code/Stats directory and execute the chi2.py script using the command: _python3 chi2.py_. This will print the p-value of the chi2 analysis between the catergories year and financially independent.
3. In the same Source-Code/Stats directory, execute the anova_posthoc.py script using the command: _python3 anova_posthoc.py_. This will print the p-value and post-hoc stats for the "Annual Withdrawal Rate" and "Annual Withdrawal Amount" columns.
4. In the same Source-Code/Stats directory, execute the t_test.py script using the command: _python3 t_test.py_. This will print the p-value's for each combination of the years (2020, 2021, 2022, 2023) mixed with the columns ("Total Assets", "Total Debt", "Annual Expenses", "Total Income", "Annual Withdrawal Rate", "Annual Withdrawal Amount"). The results are stored in the Stats-Results directory, in the file called t_test_results.csv.
5. Navigate to the Source-Code/Graphing directory and execute the graph_data.py script using the command: _python3 graph_data.py_. This will produce 7 plots in the Graphs directory outlining the average yearly values of the variables expenses, debt, assets, income, withdrawal rate and withdrawal amounts.
6. In the same Source-Code/Graphing directory, execute the world_trends_analysis.py script using the command: _python3 world_trends_analysis.py_. This will produce a plot of Global GDP by year, S&P500 total return by year, and USA federal funds by year. In addition, it will print the correlation coeficients between the values in the previous step and the financial metrics in this step.
7. In the same Source-Code/Graphing directory, execute the post_hoc.py script using the command: _python3 post_hoc.py_. This will produce 12 plots which include histograms for non-transformed and transformed values of the variables expenses, debt, assets and income. In addition, this will print the Anova p-values and post-hoc analysis results for each aformentioned variable.
8. Navigate to the Source-Code/Machine-Learning directory and execute the predict_num_fi_2020.py script using the command: _python3 predict_num_fi_2020.py_. This will produce 3 data sets in the Predicted-Data directory that uses machine learning to predict whether respondents in the 2020 data set would be financially independent in the years 2021, 2022 and 2023. In addition, validation scores for years 2021, 2022 and 2023 will be printed. 
9. In the same Source-Code/Machine-Learning directory, execute the predict_2024.py script using the command: _python3 predict_2024.py_. This will produce 8 unique graphs that use both linear and polynomial regression, as well as the t_test_results.csv file to predict the values for 2024 for the following columns: "Total Assets", "Total Debt", "Annual Expenses", "Total Income". 
10. Navigate to the Source-Code/Stats directory, execute the chi2_predicted.py script using the command: _python3 chi2_predicted.py_. This will print the p-value for the yearly predicted chi-squared test. This will say whether the number of financially independent people in the predicted data depends on the year used to train the model.
