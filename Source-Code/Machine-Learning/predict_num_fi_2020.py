import pandas as pd
import pathlib
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier

# Drop non numeric columns and columns with lots of NaNs
# Adopted from 
# https://stackoverflow.com/questions/48817592/how-to-drop-dataframe-columns-based-on-dtype
def filter_non_numeric_columns(data: pd.DataFrame):
    drop_cols = ['Children Currently', 'Children Desired', 'FI Number [Retired]', 'Annual Withdrawal Rate',
                 'Annual Withdrawal Amount', 'Year']
    fi_col = data['Financially Independent']
    data = data.select_dtypes(include=['int','float']).drop(columns=drop_cols, errors='ignore')
    data['Financially Independent'] = fi_col
    return data


def create_model(data: pd.DataFrame):
    data = data[data['Financially Independent'].isna() == False]
    y = data['Financially Independent'].values
    X = data.drop(columns='Financially Independent').fillna(0).values
    X_train, X_valid, y_train, y_valid = train_test_split(X,y)
    
    model = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(n_estimators=400, max_depth=10)
    )
    model.fit(X_train,y_train)
    score = model.score(X_valid,y_valid)
    return model, score

def make_predictions(model, data: pd.DataFrame):
    X = data.drop(columns='Financially Independent').fillna(0).values
    return model.predict(X)
    
def make_prediction_csvs(year, orig_data: pd.DataFrame, predictions: pd.Series, dir):
    orig_data['Financially Independent'] = predictions[year]
    filename = 'predicted-{year}-data.csv'.format(year=year)
    orig_data.to_csv(dir / filename, index=False)    
    
def main():    
    # parent directory
    parent_dir = pathlib.Path(__file__).parents[2]

    # get clean data
    dir = pathlib.Path(parent_dir/ 'Clean-Data')
    data_2020 = pd.read_csv(dir/'clean-2020-data.csv')
    data_2021 = pd.read_csv(dir/'clean-2021-data.csv')
    data_2022 = pd.read_csv(dir/'clean-2022-data.csv')
    data_2023 = pd.read_csv(dir/'clean-2023-data.csv')

    training_years = pd.Series(['2021','2022','2023'])
    training_data = pd.Series([data_2021,data_2022,data_2023], index=training_years)
    
    # Scikit only allows numeric types to be used as features
    training_data = training_data.apply(filter_non_numeric_columns) 
    
    # Create Models for years 2021 to 2023   
    models, scores = list(zip(*training_data.apply(create_model)))
    score_series = pd.Series(scores, index=['2021','2022','2023'], name='Validation Scores')
    model_series = pd.Series(models, index=['2021', '2022', '2023'], name='Models')
    
    # Print validation scores
    print(score_series)
    
    # make Predictions
    data_2020_for_prediction = filter_non_numeric_columns(data_2020)
    predictions = model_series.apply(make_predictions, data=data_2020_for_prediction)
    dir = pathlib.Path(parent_dir/ 'Predicted-Data')
    os.makedirs(dir, exist_ok=True)
    training_years.apply(make_prediction_csvs, orig_data=data_2020.copy(), predictions=predictions, dir=dir)
    
        
if __name__ == '__main__':
    main()