import json
import plotly
import nbapy
import datetime
import warnings
import pandas as pd
import dateutil.parser
from nbapy import game
import plotly.graph_objs as go
from nbapy.scoreboard import Scoreboard
from wrangling_scripts import constants

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

    # If games have not started yet, replace the None value with 0
    for i, row in games.iterrows():
        if row['HOME_TEAM_PTS'] is None:
            games['HOME_TEAM_PTS'].fillna(value=0, inplace=True)
            games['VISITOR_TEAM_PTS'].fillna(value=0, inplace=True)

    # Create a winner column for web layout
    winners = []
    for i, value in games.iterrows():
        if value["HOME_TEAM_PTS"] > value["VISITOR_TEAM_PTS"]:
            winners.append(value["HOME_TEAM_ABBREVIATION"])
        elif value["HOME_TEAM_PTS"] < value["VISITOR_TEAM_PTS"]:
            winners.append(value["VISITOR_TEAM_ABBREVIATION"])
        else:
            winners.append('None')

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
    live_games = live_games.fillna(0)
    live_games[["HOME_TEAM_PTS", "VISITOR_TEAM_PTS"]] = live_games[["HOME_TEAM_PTS", "VISITOR_TEAM_PTS"]].astype(int)
    return live_games

def get_boxscore(game_id):
    """
    Input:
        game_id (str) - Game ID to pull box scores

    Output:
        box_score (pandas df) - Dataframe containing the box score results of Game ID

    """
    boxscore = game.BoxScore(game_id).players_stats()

    # Data cleaning
    boxscore = boxscore.fillna(0)
    float_scores = boxscore.select_dtypes('float')
    headers = boxscore.columns.values

    # Keep PCT as floats
    pct_df = float_scores.filter(regex='PCT')
    pct_cols = pct_df.columns.values
    boxscore.drop(pct_cols, axis=1, inplace=True)
    boxscore = pd.concat([boxscore, pct_df], axis=1)

    # Convert stats to ints
    int_df = float_scores.astype(int).drop(pct_cols, axis=1)
    int_cols = int_df.columns.values
    boxscore.drop(int_cols, axis=1, inplace=True)
    boxscore = pd.concat([boxscore, int_df], axis=1)

    # Keep original order of headers
    boxscore = boxscore[headers]
    team1, team2 = boxscore.groupby("TEAM_ID")

    # Game summary
    summary = game.Info(game_id).game_summary()

    return team1[1], team2[1], summary

def get_teamstats(game_id):
    """
    Input:
        game_id (str) - Game ID to pull team stats

    Output:
        team_stats (pandas df) - Dataframe showing the teams percentages

    """
    team_stats = game.BoxScore(game_id).team_stats()
    team_stats['TEAM_FULL_NAME'] = team_stats['TEAM_CITY'] + " " + team_stats['TEAM_NAME']
    team1, team2 = team_stats.groupby("TEAM_ID")
    return team1[1], team2[1]

def get_linescore(game_id):
    """
    Input:
        game_id (str) - Game ID to pull line score

    Ouput:
        line_score (pandas df) - Dataframe showing the points by quarter

    """
    line_score = game.Info(game_id).line_score()
    return line_score

def create_teamstats_barchart(game_id):
    """
    Creates two Plotly bar charts

    Input:
        game_id (str) - Game ID to pull team stats data

    Output:
        list (dict) - List containing the two Plotly visualizations
    """
    team1, team2 = get_teamstats(game_id)
    #teamstats_cols = ['TEAM_ABBREVIATION', 'REB']

    t1_name = team1['TEAM_FULL_NAME'].values[0]
    t1_id = str(team1['TEAM_ID'].values[0])
    team1 = team1[['REB', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TO']]
    df1 = team1.T.reset_index().rename(columns={'index':'Columns', 1:'Count'})

    t2_name = team2['TEAM_FULL_NAME'].values[0]
    t2_id = str(team2['TEAM_ID'].values[0])
    team2 = team2[['REB', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'TO']]
    df2 = team2.T.reset_index().rename(columns={'index':'Columns', 0:'Count'})

    data1 = [
        go.Bar(
            x=df1['Columns'], # assign x as the dataframe column 'x'
            y=df1['Count'],
            name=t1_name,
            marker={
                'color': constants.TEAM_ID_TO_NAME[t1_id]['color']
            }
            )
        ]

    data2 = [
        go.Bar(
            x=df2['Columns'], # assign x as the dataframe column 'x'
            y=df2['Count'],
            name=t2_name,
            marker={
                'color': constants.TEAM_ID_TO_NAME[t2_id]['color']
            }
            )
        ]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    res1 = json.loads(graphJSON1)
    res2 = json.loads(graphJSON2)

    return res1[0], res2[0]

def create_teampct_barchart(game_id):
    """
    Creates two Plotly bar charts

    Input:
        game_id (str) - Game ID to pull team stats data

    Output:
        list (dict) - List containing the two Plotly visualizations
    """
    team1, team2 = get_teamstats(game_id)
    #teamstats_cols = ['TEAM_ABBREVIATION', 'REB']

    t1_name = team1['TEAM_ABBREVIATION'].values[0]
    t1_id = str(team1['TEAM_ID'].values[0])
    team1 = team1[['FG_PCT', 'FG3_PCT', 'FT_PCT']]
    df1 = team1.T.reset_index().rename(columns={'index':'Columns', 1:'Count'})

    t2_name = team2['TEAM_ABBREVIATION'].values[0]
    t2_id = str(team2['TEAM_ID'].values[0])
    team2 = team2[['FG_PCT', 'FG3_PCT', 'FT_PCT']]
    df2 = team2.T.reset_index().rename(columns={'index':'Columns', 0:'Count'})

    data1 = [
        go.Bar(
            x=df1['Columns'], # assign x as the dataframe column 'x'
            y=df1['Count'],
            name=t1_name,
            marker={
                'color': constants.TEAM_ID_TO_NAME[t1_id]['color']
            }
            )
        ]

    data2 = [
        go.Bar(
            x=df2['Columns'], # assign x as the dataframe column 'x'
            y=df2['Count'],
            name=t2_name,
            marker={
                'color': constants.TEAM_ID_TO_NAME[t2_id]['color']
            }
            )
        ]

    graphJSON1 = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)

    res1 = json.loads(graphJSON1)
    res2 = json.loads(graphJSON2)

    return res1[0], res2[0]
