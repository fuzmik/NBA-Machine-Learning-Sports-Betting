import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
import xgboost as xgb
from tqdm import tqdm

# Load dataset from SQLite database
dataset = "dataset_2012-24_new"
con = sqlite3.connect("Data/dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()

# Separate the target variable (margin) and drop unnecessary columns
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 
           'TEAM_NAME.1','Date.1', 'OU-Cover', 'OU'], axis=1, inplace=True)

# Convert data to float type for numerical computations
data = data.astype(float)

kf = KFold(n_splits=300) # Perform 5-fold cross validation
# Initialize acc_results as a list of size n filled with zeroes
n = len('../../Models/XGBoost_68.9%_ML-3.json') # replace this with your actual data length or number
acc_results = []*n

for train_index, test_index in tqdm(kf.split(data)):   # Loop over each split of the data
    x_train, x_test = data.iloc[train_index], data.iloc[test_index]
    y_train, y_test = margin.iloc[train_index], margin.iloc[test_index]
    
    # Convert pandas DataFrames to XGBoost DMatrix
    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)
    
    # Parameters for the XGBoost model
    param = {
        'max_depth': 3,   # Optimization: Reduce maximum depth of tree to avoid overfitting
        'eta': 0.1,         # Optimal learning rate for a fast converging model
        'objective': 'multi:softprob',
        'num_class': 2,
        'early_stopping_rounds': 50   # Early stopping after 5 rounds of no improvement
    }
    
    epochs = 750                # Number of iterations (epochs) to train the model

    # Train the XGBoost model and make predictions
    watchlist = [(train, 'train'), (test, 'eval')]  # Setup for evaluation metrics
    model = xgb.train(param, train, epochs, evals=watchlist)
    
    predictions = model.predict(test)
    y = []
    for z in predictions:
        y.append(np.argmax(z))  # Decode one-hot encoded labels to get class label

    acc = round(accuracy_score(y_test, y) * 100, 1)     # Calculate accuracy score
    
    print("Accuracy: {}%".format(acc))
    
    # Now, each time after calculating accuracy (acc), append it into the result
    acc_results.append(acc)

    # ... snip ...
    if acc > max(acc_results):     
       model.save_model('../../Models/XGBoost_{}%_ML-4.json'.format(acc))  # Save the current model
    elif acc == max(acc_results) and len(acc_results) > 1:                  # If it is a tie with an existing maximum, save it under another name
       model.save_model('../../Models/XGBoost_{}%_ML-{}-4-tie.json'.format(acc)) 
    # ... snip ...
    

