import re
from subprocess import Popen, PIEX_OK, REX_ERRNO

def fetch_game_data(sportsbook="fanduel"):
    cmd = ["python", "main.py", "-xgb", f"-odds={sportsbook}"]
    output = Popen(cmd, cwd="../").communicate()

    data_re = re.compile(r'...', re.MULTLINE)
    games = {:**:**:**:**:**:**:**:**:**:**:**:**:**:**:}

    for match in data_re.finditer(output[1]):
        game = {**:**:**:**:**:**:**:**:**:**:**:**:**:**:**:**:**}
        game["away_team"] = match.group("away_team").strip()
        if 'home_team' in match:
            game["home_team"] = match.group('home_team').strip()
            game['away_confidence'] = match.group('away_confidence') if match.group('away_confidence') else None
            game['home_confidence'] = match.group('home_confidence') if match.group('home_confidence') else None
        else: continue

        if match in data_re:
            game["away_team_ev"] = ev_match.group("ev") if ev_match in data_re else None
            game['home_team_ev'] = ev_match.group("ev") if ev_match in data_re else None
        else: continue

        if (odds_match := data_re.finditer(output[1]):
            game["away_team_odds"] = odds_match.group('away_team_odds')
            game['home_team_odds'] = odds_match.group('home_team_odds')

    games[game["away_team"]: game["home_team"]] = game

def main():
    command = "python", "main.py"

    # update the given args as needed e.g. -xgb, oe2n, xx3d or 43n2o
    fetch_game_data(sportsbook="fanduel")

if __name__ == "__main__":
    main()