import numpy as np
import pandas as pd

## Minimum number of games played Filter
# Only pick players that have played in 20 games
def min_games_filter(df):
    # Minimum threshoold for number of games played
    half_filter = (df.PLAYER.value_counts() > 15)
    half_df = pd.DataFrame(half_filter).reset_index().rename({'index':'PLAYER','PLAYER':'HalfSeason'}, axis=1)
    invalid_df = half_df[half_df['HalfSeason'] == False].drop('HalfSeason', axis=1)
    output_df = pd.merge(df, invalid_df, on='PLAYER', how='left', indicator=True).query("_merge == 'left_only'").drop('_merge',1)
    return output_df

def ohe_players(df):
    df = pd.merge(df, pd.get_dummies(df['PLAYER'], prefix='PLAYER'), left_index=True, right_index=True)
    df = df.drop("PLAYER", axis=1)
    return df

## Data Cleaning
def clean_nulls(raw_df, drop_date):
    # Cleans the nulls in the Position columns
    cat_df = raw_df.filter(regex=('POSITION')).fillna('None')
    raw_df = raw_df.drop(raw_df.filter(regex=('POSITION')), axis=1)
    clean_df = pd.merge(raw_df, cat_df, left_index=True, right_index=True)

    # Clean the nulls in the salary columns with their averages
    clean_df.DRAFTKINGS_CLASSIC_SALARY = clean_df.DRAFTKINGS_CLASSIC_SALARY.fillna(clean_df['DRAFTKINGS_CLASSIC_SALARY'].mean())
    clean_df.FANDUEL_FULLROSTER_SALARY = clean_df.FANDUEL_FULLROSTER_SALARY.fillna(clean_df['FANDUEL_FULLROSTER_SALARY'].mean())
    clean_df.YAHOO_FULLSLATE_SALARY = clean_df.YAHOO_FULLSLATE_SALARY.fillna(clean_df['YAHOO_FULLSLATE_SALARY'].mean())

    # Clean the days rest column
    clean_df.DAYSREST = clean_df.DAYSREST.replace(to_replace='3+', value=4)

    if drop_date == True:
        clean_df = clean_df.drop('DATE', axis=1)
    else:
        # Data clean the date columns
        clean_df['DATE_Month'] = pd.DatetimeIndex(clean_df['DATE']).month_name()
        clean_df['DATE_Day'] = pd.DatetimeIndex(clean_df['DATE']).day
        clean_df['DATE_Year'] = pd.DatetimeIndex(clean_df['DATE']).year
        clean_df[['DATE_Month', 'DATE_Day', 'DATE_Year']] = clean_df[['DATE_Month', 'DATE_Day', 'DATE_Year']].astype(object)
        clean_df = clean_df.drop('DATE', axis=1)

    return clean_df

## Feature Engineering
def prepare_dataset(input, dfs_type):
    # Data cleaning the variables
    input = input.drop(["DATASET"], axis=1)

    # Clean the numerical columns
    num_df = input.select_dtypes(include=['float64', 'int64'])
    num_df = num_df.drop(['PLAYER-ID', 'GAME-ID'], axis=1)

    # Clean up the object columns
    object_df = input.select_dtypes(include=['object'])
    dum_object_df = pd.get_dummies(object_df)

    # Final clean up
    prep_df = pd.merge(num_df, dum_object_df, left_index=True, right_index=True)

    # Add the player columns
    player_df = input.filter(regex=("PLAYER_"))
    finalprep_df = pd.merge(prep_df, player_df, left_index=True, right_index=True)

    # Filter out the Fantasy columns
    yahoo_cols = finalprep_df.filter(regex=('YAHOO'))
    draftkings_cols = finalprep_df.filter(regex=('DRAFTKINGS'))
    fanduel_cols = finalprep_df.filter(regex=('FANDUEL'))

    # DFS columns only
    yahoo_df = finalprep_df.drop(draftkings_cols.columns.values, axis=1).drop(fanduel_cols.columns.values, axis=1)
    draftkings_df = finalprep_df.drop(yahoo_cols.columns.values, axis=1).drop(fanduel_cols.columns.values, axis=1)
    fanduel_df = finalprep_df.drop(draftkings_cols.columns.values, axis=1).drop(yahoo_cols.columns.values, axis=1)

    if dfs_type == "YH":
        return yahoo_df
    elif dfs_type == "DK":
        return draftkings_df
    else:
        return fanduel_df

# Get feature importances
def get_feature_importance(regressor, col_names, num_features):
    # Get numerical feature importances
    importances = list(regressor.feature_importances_)

    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 20)) for feature, importance in zip(col_names, importances)]

    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse=True)
    feature_importance_df = pd.DataFrame(feature_importances, columns=['Feature', 'Importance'])
    return feature_importance_df.head(num_features)

#################### Notes #####################################################
# Sample set vs test set by dates
# sample_filter = (df['DATE'] <= '2019-03-01')
# sample_set = df[sample_filter]
# print(sample_set.shape)
# sample_set.head()

# Test set
# test_filter = (df['DATE'] > '2019-03-01')
# test_sample = df[test_filter]
# print(test_sample.shape)
# test_sample.head()

# First predictions
# # Predict on Yahoo Fantasy Points
# X = finalprep_df.drop(['YAHOO_FANTASYPOINTS'], axis=1).values
# y = finalprep_df['YAHOO_FANTASYPOINTS'].values

# # Keep the dependent feature names
# X_colnames = finalprep_df.drop(['YAHOO_FANTASYPOINTS'], axis=1).columns
# X_colnames




#################### Model Evaluation ##########################################
## Testing the model
# # Forest Predict method
# predictions = rf_regressor.predict(X_test_std)

# # Calculate absolute errors
# errors = abs(predictions - y_test)

# # Print out the mean absolute error (MAE)
# print("Mean Absolute Error:", round(np.mean(errors), 2), 'degrees.')

# # Calculate mean absolute percentage error (MAPE)
# mape = 100 * (errors / y_test)

# # Calculate and display accuracy
# accuracy = 100 - np.mean(mape)

# print('Accuracy:', round(accuracy, 2), '%.')

# # Create confusion matrix
# pd.crosstab(test['species'], preds, rownames=['Actual Species'], colnames=['Predicted Species'])
