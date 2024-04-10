import argparse
import json
import time
import requests
import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import xgboost as xgb
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings('ignore')
from tqdm import tqdm

class TeamIndex():
    def __init__(self):
        self.index = {}
        
    def add(self, team, index):
        self.index[team] = index

def fetch_odds(sportsbook, sport_id, game_id):
    # Your API call implementation here to fetch the odds data

def preprocess():
    data = json.load(open('data.json'))
    team_idx = TeamIndex()
    for line in data:
        game_details = json.loads(line)
        start_time = datetime.strptime(game_details['StartTime'], '%Y-%m-%d %H:%M:%S')
        game_id = int(game_details['GameID'])
        home_team = game_details['Teams']['@id'][:-1] # remove the '/' character
        away_team = game_details['Teams'][1]['@id'][:-1] # remove the '/' character
        team_idx.add(home_team, start_time)
        team_idx.add(away_team, start_time)

    preprocessed_data = []
    for game_details in data:
        start_time = datetime.strptime(game_details['StartTime'], '%Y-%m-%d %H:%M:%S')
        game_id = int(game_details['GameID'])
        home_team = team_idx[game_details['Teams'][0]['@id'][:-1]]
        away_team = team_idx[game_details['Teams'][1]['@id'][:-1]]
        preprocessed_data.append({'start_time': start_time, 'game_id': game_id, 'home_team': home_team, 'away_team': away_team})
        
    return preprocessed_data

def parse_game_details(game_data):
    home_win = 0 if game_data['Spread']['Result'][-1] == '-' else int(game_data['Spread']['Result'])
    away_win = 0 if game_data['ML']['Result'][-1] == '-' else int(game_data['ML']['Result'])

    home_team = game_data['Teams'][0]['@id'][:-1] # remove the '/' character
    away_team = game_data['Teams'][1]['@id'][:-1]  # remove the '/' character
    
    return {'game_id': game_data['GameID'], 'home_team': home_team, 'away_team': away_team, 'home_win': home_win, 'away_win': away_win}

def fetch_todays_games(sportsbook):
    # Your implementation to scrape todays games data goes here

def load_model():
    X_train = np.load('X_train.npy')
    y_train = np.load('y_train.npy')

    xgb_clf = xgb.XGBClassifier(objective='binary:softmax', num_classes=2, n_estimators=50, learning_rate=0.1)
    xgb_clf.fit(X_train, y_train)
    
    nn_clf = MLPClassifier(hidden_layer_sizes=(100, 100), activation='relu', max_iter=500)
    return xgb_clf, nn_clf

def main():
    parser = argparse.ArgumentParser(description='Model to Run')
    parser.add_argument('-xgb', action='store_true', help='Run with XGBoost Model')
    parser.add_argument('-nn', action='store_true', help='Run with Neural Network Model')
    parser.add_argument('-A', action='store_true', help='Run all Models')
    parser.add_argument('-odds', help='Sportsbook to fetch from. (fanduel, draftkings, betmgm, pointsbet, caesars, wynn, bet_rivers_ny)')
    parser.add_argument('-kc', action='store_true', help='Calculates percentage of bankroll to bet based on model edge')
    args = parser.parse_args()
    
    start = time.time()

    if args.odds:
        # Fetching odds data from the specified sportsbook API
        odds_data = fetch_odds(args.odds)
    else:
        odds_data = []
        
    preprocessed_games = preprocess()

    if not args.xgb and not args.nn and not args.A:
        print('No model to run')
        return
    
    X, y = [], []
    for game_data in preprocessed_games:
        parsed_game_details = parse_game_details(game_data)
        X.append([parsed_game_details['home_win'], parsed_game_details['away_win']])
        y.append(1 if parsed_game_details['home_team'] < parsed_game_details['away_team'] else 0)
        
    np.save('X.npy', X)
    np.save('y.npy', y)
    
    if args.xgb:
        xgb_clf, nn_clf = load_model()
        xgb_preds = xgb_clf.predict(np.array(X))
        xgb_acc = np.sum(xgb_preds == y) / len(y)
        print('XGBoost Model accuracy: {}'.format(xgb_acc))
        
    if args.nn:
        nn_clf = load_model()[1]
        nn_preds = nn_clf.predict(np.array(X))
        nn_acc = np.sum(nn_preds == y) / len(y)
        print('Neural Network Model accuracy: {}'.format(nn_acc))
        
    if args.A:
        xgb_clf, nn_clf = load_model()
        xgb_preds = xgb_clf.predict(np.array(X))
        xgb_acc = np.sum(xgb_preds == y) / len(y)
        print('XGBoost Model accuracy: {}'.format(xgb_acc))
        nn_preds = nn_clf.predict(np.array(X))
        nn_acc = np.sum(nn_preds == y) / len(y)
        print('Neural Network Model accuracy: {}'.format(nn_acc))
        
    if args.kc:
        # Implementation for calculating the percentage of bankroll to bet based on model edges goes here
        
    elapsed = time.time() - start
    print('Elapsed time: {}s'.format(elapsed))

if __name__ == '__main__':
    main()
