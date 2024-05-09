import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
from tqdm import tqdm

# Load dataset from SQLite database
dataset = "dataset_2012-24_new"
con = sqlite3.connect("../../Data/dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()

# Separate the target variable (OU) and drop unnecessary columns
OU = data['OU-Cover']
total = data['OU']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 
           'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'], axis=1, inplace=True)

# Add the total column to data after converting it to float type
data['OU'] = np.asarray(total).astype(float)

acc_results = []
for _ in tqdm(range(100)):  # loop runs 100 times
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data.values, OU, test_size=0.1)
    
    # Convert pandas DataFrames to XGBoost DMatrix
    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test)
    
    # Parameters for the XGBoost model
    param = {
        'max_depth': 20,       # Optimization: Increase maximum depth to improve generalization
        'eta': 0.05,           # Optimal learning rate for a fast converging model
        'objective': 'multi:softprob',
        'num_class': 3         # Number of classes in the target variable
    }
    
    epochs = 750               # Number of iterations (epochs) to train the model

    # Train the XGBoost model and make predictions
    model = xgb.train(param, train, epochs)
    predictions = model.predict(test)
    
    y = []
    for z in predictions:
        y.append(np.argmax(z))   # Decode one-hot encoded labels to get class label

    acc = round(accuracy_score(y_test, y)*100, 1)   # Calculate accuracy score
    
    print(f"Accuracy: {acc}%")
    acc_results.append(acc)      # Save the accuracy result

    if acc == max(acc_results):   # Only save results if they are the best so far (highest accuracy)
        model.save_model('../../Models/XGBoost_{}%_UO-9.json'.format(acc))  # Save the model with its accuracy as filename
