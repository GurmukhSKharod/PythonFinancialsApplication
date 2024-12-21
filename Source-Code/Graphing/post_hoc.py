import pandas as pd
import pathlib
from scipy import stats
import matplotlib.pyplot as plot
import os
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def get_data(parent_dir, columns, years):
    dir = pathlib.Path(parent_dir/ 'Clean-Data')
    data_2020 = pd.read_csv(dir/'clean-2020-data.csv', usecols=columns).loc[:,columns]
    data_2021 = pd.read_csv(dir/'clean-2021-data.csv', usecols=columns).loc[:,columns]
    data_2022 = pd.read_csv(dir/'clean-2022-data.csv', usecols=columns).loc[:,columns]
    data_2023 = pd.read_csv(dir/'clean-2023-data.csv', usecols=columns).loc[:,columns]
    return pd.Series([data_2020,data_2021,data_2022,data_2023], index=years)
    
    
def generate_histograms(column: str, title: str, data, parent_dir):
    bins = 50
    fig, ax = plot.subplots(2,2, figsize=(10, 8))
    ax[0][0].hist(data['2020'][column], alpha=0.5, bins=bins)
    ax[0][0].set_title('2020')
    ax[0][1].hist(data['2021'][column], alpha=0.5, bins=bins)
    ax[0][1].set_title('2021')
    ax[1][0].hist(data['2022'][column], alpha=0.5, bins=bins)
    ax[1][0].set_title('2022')
    ax[1][1].hist(data['2023'][column], alpha=0.5, bins=bins)
    ax[1][1].set_title('2023')
    
    graph_dir = pathlib.Path(parent_dir/ 'Graphs')
    os.makedirs(graph_dir, exist_ok=True)
    
    fig.suptitle(title + ' of ' + column, fontsize=20)
    fig.supxlabel(column)
    fig.supylabel('Count')
    plot.savefig(graph_dir/'{title}_of_{column}.png'.format(column=column.replace(' ','_').lower(),
                                                            title=title.replace(' ','_').lower()))

def sqrt_transform_data(data):   
    return np.sqrt(data)
    
def post_hoc_pipeline(column: str, title: str, data, parent_dir):    
    anova = stats.f_oneway(data['2020'][column].dropna(), data['2021'][column].dropna(), 
                           data['2022'][column].dropna(),data['2023'][column].dropna())
    print('{title} {column} Anova value:'.format(column=column, title=title), anova.pvalue)
    
    combined_data = pd.DataFrame({'2020':data['2020'][column],
                          '2021':data['2021'][column],
                          '2022':data['2022'][column],
                          '2023':data['2023'][column]
                          })
    combined_melt = pd.melt(combined_data).dropna()
    posthoc = pairwise_tukeyhsd(
        combined_melt['value'], combined_melt['variable'], alpha=0.05
    )
    print('{title} Post Hoc of {column}'.format(column=column, title=title))
    print(posthoc)
    

def drop_null_zero_rows(d: pd.DataFrame):
    return d[(d['Total Assets'] != 0) | (d['Total Debt'] != 0) | 
             (d['Annual Expenses'] != 0) | (d['Total Income'] != 0)].reset_index(drop=True)
        
def main():    
    # parent directory
    parent_dir = pathlib.Path(__file__).parents[2]

    # data columns to perform post-hoc analysis on
    columns = pd.Series(['Total Assets','Total Debt','Annual Expenses','Total Income'])

    # data years
    years = pd.Series(['2020','2021','2022','2023'])
    # get clean data
    
    data = get_data(parent_dir, columns, years)
    # check if distribution is normal for each year of a given column
    columns.apply(generate_histograms, title='Yearly Histograms', data=data, parent_dir=parent_dir)
    # Perform post-hoc analysis on non-transformed data (probably not a good idea because it's very skewed)
    # columns.apply(post_hoc_pipeline, title='',  data=data, parent_dir=parent_dir)
    
    # attempt to de-skew by removing rows with all zeroes
    data_zero_dropped = data.apply(drop_null_zero_rows)
    columns.apply(generate_histograms, title='Zeroes Dropped Yearly Histograms', data=data_zero_dropped, 
                  parent_dir=parent_dir)
    
    # Perform post-hoc analysis on zero-row dropped data (probably not a good idea because it's still skewed)
    # columns.apply(post_hoc_pipeline, title='Zeroes Dropped',  data=data_zero_dropped, parent_dir=parent_dir)

    # distribution is still skewed-right for all columns, so apply a sqrt transformation instead
    data_transformed = data_zero_dropped.apply(sqrt_transform_data)
    
    # check if distribution is normal for transformed data
    columns.apply(generate_histograms, title='Sqrt Transformed Yearly Histograms', data=data_transformed,
                  parent_dir=parent_dir)
    
    # Perform post-hoc analysis on transformed data
    columns.apply(post_hoc_pipeline, title='Sqrt Transformed', data=data_transformed, parent_dir=parent_dir)
    
if __name__ == '__main__':
    main()