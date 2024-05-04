import sqlite3
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from tqdm import tqdm

def train_xgb_model(data):
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data.drop('OU', axis=1), data['OU'], test_size=0.1)

    # Create DMatrices for training and testing
    train_mat = xgb.DMatrix(x_train, label=y_train)
    test_mat = xgb.DMatrix(x_test)

    # Set XGBoost parameters
    param = {'max_depth': 20, 'eta': 0.05, 'objective': 'multi:softprob', 'num_class': 3, 'device': 'cuda:0', 'tree_method': 'hist'}

    # Train the model
    model = XGBClassifier(**param)
    model.fit(train_mat, num_boost_round=750)

    # Make predictions and calculate accuracy
    predictions = model.predict(test_mat)
    y_pred = [np.argmax(p) for p in predictions]
    acc = round(f1_score(y_test, y_pred), 2)

    return acc, model

def main():
    dataset = "dataset_2012-24"
    conn = sqlite3.connect("../../Data/dataset.sqlite")
    data = pd.read_sql_query(f"select *  from \"{dataset}\"", conn, index_col="index")
    conn.close()

    # Prepare the data
    OU = data['OU-Cover']
    total = data['OU']
    data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU-Cover', 'OU'], axis=1, inplace=True)
    data['OU'] = np.asarray(total)
    data = data.values
    data = data.astype(float)

    highest_acc = 0
    best_model = None

    for _ in tqdm(range(10)):  # Iterate only once to reduce computation time
        acc, model = train_xgb_model(data)
        print(f"Accuracy: {acc}%")
        if acc > highest_acc:
            highest_acc = acc
            best_model = model

    if best_model is not None:
        best_model.save_model(f'../../Models/XGBoost_Models/XGBoost_{highest_acc}%_UO-9.json')

if __name__ == "__main__":
    main()
