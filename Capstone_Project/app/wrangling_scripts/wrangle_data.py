import nbapy
import datetime
import warnings
import pandas as pd
import dateutil.parser
from nbapy import game
from nbapy.scoreboard import Scoreboard

pd.set_option('max_columns', None)
pd.options.mode.chained_assignment = None

def get_games(datestring):
    """
    Input:
        datestring (str) - date of NBA games to grab

    Output:
        games (pandas df) - dataframe of NBA games, results, and teams playing

    """
    date = dateutil.parser.parse(datestring)
    scoreboard = Scoreboard(date.month, date.day, date.year)

    # Grab today's game information
    game_header = scoreboard.game_header()
    line_score = scoreboard.line_score()

    # Simplify columns
    games = game_header[['GAME_SEQUENCE', 'GAME_ID', 'GAME_STATUS_TEXT',
                         'LIVE_PERIOD', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID',
                         'NATL_TV_BROADCASTER_ABBREVIATION']]
    score = line_score[['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PTS']]

    # Dictionary of game values
    team_info = score.set_index('TEAM_ID')['TEAM_ABBREVIATION'].to_dict()
    team_pts = score.set_index('TEAM_ID')['PTS'].to_dict()

    # Map to games info
    games['HOME_TEAM_ABBREVIATION'] = games.HOME_TEAM_ID.map(team_info)
    games['VISITOR_TEAM_ABBREVIATION'] = games.VISITOR_TEAM_ID.map(team_info)
    games['HOME_TEAM_PTS'] = games.HOME_TEAM_ID.map(team_pts)
    games['VISITOR_TEAM_PTS'] = games.VISITOR_TEAM_ID.map(team_pts)

    # Create a winner column for web layout
    winners = []
    for i, value in games.iterrows():
        if (value["HOME_TEAM_PTS"] > value["VISITOR_TEAM_PTS"]):
            winners.append(value["HOME_TEAM_ABBREVIATION"])
        elif (value["HOME_TEAM_PTS"] < value["VISITOR_TEAM_PTS"]):
            winners.append(value["VISITOR_TEAM_ABBREVIATION"])
        else:
            winners.append(None)

    games['WINNER'] = winners

    return games

def get_livegames():
    """
    Input:
        None

    Output:
        live_games (pandas df) - Dataframe showing results for today's NBA games
    """
    today = datetime.datetime.now()
    today_string = today.strftime("%m-%d-%Y")
    live_games = get_games(today_string)
    return live_games

def get_boxscore(game_id):
    """
    Input:
        game_id (str) - Game ID to pull box scores

    Output:
        box_score (pandas df) - Dataframe containing the box score results of Game ID

    """
    box_score = game.BoxScore(game_id).players_stats()
    return box_score

def get_teamstats(game_id):
    """
    Input:
        game_id (str) - Game ID to pull team stats

    Output:
        team_stats (pandas df) - Dataframe showing the teams percentages

    """
    team_stats = game.BoxScore(game_id).team_stats()
    return team_stats

def get_linescore(game_id):
    """
    Input:
        game_id (str) - Game ID to pull line score

    Ouput:
        line_score (pandas df) - Dataframe showing the points by quarter

    """
    line_score = game.Info(game_id).line_score()
    return line_score
