import argparse
import json
from datetime import datetime, timedelta

from colorama import Fore, Style

from nn_runner import NN_Runner
from xgboost_runner import XGBoost_Runner

data_url = "https://raw.githubusercontent.com/JeffreySunMR/MLB-Odds-Predictor/main/datasets/mlb_stats.json"
todays_games_url = "https://www.sportsbookreviewed.com/mma-betting-odds/"

args = None


def get_json_data(url):
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    return data


def to_data_frame(data):
    df = pd.DataFrame(data, columns=['Date', 'HomeTeam', 'AwayTeam'])
    return df


def createTodaysGames(games, df, odds):
    match_data = []
    todays_games_uo = {}
    home_team_odds = {}
    away_team_odds = {}
    for g in games:
        home_team = g[0]
        away_team = g[1]
        if odds is not None:
            home_team_odds[g] = odds.get(home_team, {})['money_line_odds']
            away_team_odds[g] = odds.get(away_team, {})['money_line_odds']
        team_index_current = {}
        for i in range(len(df)):
            if df['HomeTeam'].iloc[i] == home_team:
                team_index_current['HomeTeam'] = i
            elif df['AwayTeam'].iloc[i] == away_team:
                team_index_current['AwayTeam'] = i
        previous_home_games = df.loc[df['HomeTeam'] == home_team]['Date']
        previous_away_games = df.loc[df['AwayTeam'] == away_team]['Date']
        todays_games_uo[home_team] = [x for x in previous_home_games if (datetime.today().date() - datetime(x).date()).days <= 1]
        todays_games_uo[away_team] = [x for x in previous_away_games if (datetime.today().date() - datetime(x).date()).days <= 1]
        home_index = team_index_current['HomeTeam']
        away_index = team_index_current['AwayTeam']
        previous_home_wins = df.loc[df['Date'] == previous_home_games, 'WinColumn'].values
        previous_away_wins = df.loc[df['Date'] == previous_away_games, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam'] == away_team, 'WinColumn'].values
        if home_index != None:
            previous_home_wins = previous_home_wins[0]
        else:
            previous_home_wins = 0
        if away_index != None:
            previous_away_wins = previous_away_wins[0]
        else:
            previous_away_wins = 0
        home_win = df.loc[df['HomeTeam'] == home_team, 'WinColumn'].values
        away_win = df.loc[df['AwayTeam^C
