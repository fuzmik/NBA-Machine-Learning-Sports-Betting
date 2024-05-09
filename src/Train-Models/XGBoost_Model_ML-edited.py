import sqlite3
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Load dataset from SQLite database
dataset = "dataset_2012-24_new"
con = sqlite3.connect("../../Data/dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()

# Separate the target variable (margin) and drop unnecessary columns
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 
           'TEAM<｜begin▁of▁sentence｜>_NAME.1','Date.1', 'OU-Cover', 'OU'], axis=1, inplace=True)

# Convert data to float type for numerical computations
data = data.astype(float)

acc_results = []
for _ in tqdm(range(300)):   # loop runs 300 times
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=.1)
    
    # Convert pandas DataFrames to XGBoost DMatrix
    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)
    
    # Parameters for the XGBoost model
    param = {
        'max_depth': 3,       # Optimization: Reduce maximum depth of tree to avoid overfitting
        'eta': 0.1,            # Optimal learning rate for a fast converging model
        'objective': 'multi:softprob',
        'num_class': 2
    }
    
    epochs = 750               # Number of iterations (epochs) to train the model

    # Train the XGBoost model and make predictions
    model = xgb.train(param, train, epochs)
    predictions = model.predict(test)
    
    y = []
    for z in predictions:
        y.append(np.argmax(z))   # Decode one-hot encoded labels to get class label

    acc = round(accuracy_score(y_test, y) * 100, 1)    # Calculate accuracy score
    
    print(f"Accuracy: {acc}%")
    
    if acc > max(acc_results):    # Only save results if they are the best so far (higher accuracy)
        model.save_model('../../Models/XGBoost_{}%_ML-4.json'.format(acc))   # Save the model with its accuracy as filename
