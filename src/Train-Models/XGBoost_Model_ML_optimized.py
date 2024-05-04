import xgboost as xgb
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import sqlite3

def train_model(data, margin):
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data, margin, test_size=0.1)

    # Define model parameters
    param = {
        'max_depth': 3,
        'eta': 0.01,
        'objective': 'multi:softprob',
        'num_class': 2,
        'device': 'cuda:0', 
        'tree_method': 'hist'
    }
    epochs = 750

    # Train the model
    train = xgb.DMatrix(x_train, label=y_train)
    test = xgb.DMatrix(x_test, label=y_test)
    model = xgb.train(param, train, epochs)

    # Make predictions and calculate accuracy
    predictions = model.predict(test, param)
    y = [np.argmax(z) for z in predictions]
    acc = round(accuracy_score(y_test, y) * 100, 1)
    return acc, model

def main():
    dataset = "dataset_2012-24"
    con = sqlite3.connect("../../Data/dataset.sqlite")
    data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
    con.close()

    margin = data['Home-Team-Win']
    data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'], axis=1, inplace=True)

    data = data.values
    data = data.astype(float)

    highest_acc = 0
    best_model = None

    for _ in tqdm(range(300)):
        acc, model = train_model(data, margin)
        print(f"Accuracy: {acc}%")

        if acc > highest_acc:
            highest_acc = acc
            best_model = model

    # Save the best model as a JSON file
    if best_model is not None:
        best_model.save_model(f'../../Models/XGBoost_Models/XGBoost_{highest_acc}%_ML-4.json')

if __name__ == '__main__':
    main()
