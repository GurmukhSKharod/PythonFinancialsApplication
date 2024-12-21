import pandas as pd
from scipy import stats
import pathlib

import matplotlib.pyplot as plot
import os
import numpy as np


#returns 1d array in the format [#of FI, #non FI]
def get_counts(data):
    fi = data[data['Financially Independent']== 'Yes'] 
    not_fi = data[data['Financially Independent']== 'No'] 
    counts = np.array([fi['Financially Independent'].size, not_fi['Financially Independent'].size])
    return counts

#returns our data in the contingency format needed for chi2
def prep_data():
    #just took this file reading from jostin
    parent_dir = pathlib.Path(__file__).parents[2]
    dir = pathlib.Path(parent_dir/ 'Predicted-Data')
    data_2021 = pd.read_csv(dir/'predicted-2021-data.csv')
    data_2022 = pd.read_csv(dir/'predicted-2022-data.csv')
    data_2023 = pd.read_csv(dir/'predicted-2023-data.csv')


    return np.array([get_counts(data_2021),get_counts(data_2022),get_counts(data_2023)])


def main():
    #get data in the format we need
    contingency = prep_data()
    #perfrom the chi2 test
    chi2 = stats.chi2_contingency(contingency)
    #if we get a pvalue < 0.05 then there is some significance in the year
    print(chi2.pvalue)



if __name__ == '__main__':
    main()