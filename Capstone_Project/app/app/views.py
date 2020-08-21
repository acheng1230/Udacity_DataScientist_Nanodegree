from app import app
from flask import render_template, request, redirect

import datetime
import dateutil.parser
from nbapy.scoreboard import Scoreboard
from wrangling_scripts import constants
from wrangling_scripts.wrangle_data import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores", methods=["GET"])
def scores():
    """
    NBA Scores Page (Live scores and past using Datepicker)
    """
    try:
        date_list = request.args.getlist("date-scores")
        date_string = date_list[0]
        games = get_games(date_string)

    except:
        today = datetime.datetime.now()
        date_string = today.strftime("%m/%d/%Y")
        games = get_livegames()

    return render_template("scores.html",
                           games=games,
                           constants=constants,
                           placeholder=date_string)

@app.route("/standings")
def standings():
    """
    NBA Standings Page (Western & Eastern Conferences)
    """
    scoreboard = Scoreboard()
    east_standings = scoreboard.east_conf_standings_by_day()
    west_standings = scoreboard.west_conf_standings_by_day()

    return render_template("standings.html",
                           east_standings=east_standings,
                           west_standings=west_standings)

@app.route("/boxscores/<gameid>")
def boxscores(gameid):
    """
    NBA Box Scores Page (Team Stats, Four Factors, Box Scores and Highlights)
    """
    # Team Stats
    team_stats = get_teamstats(gameid)

    # Box Scores
    team1, team2 = get_boxscore(gameid)
    team1_id = str(team1['TEAM_ID'].unique()[0])
    team1_name = constants.TEAM_ID_TO_NAME[team1_id]['team-name']
    team2_id = str(team2['TEAM_ID'].unique()[0])
    team2_name = constants.TEAM_ID_TO_NAME[team2_id]['team-name']

    return render_template("boxscores.html",
                           constants=constants,
                           team_stats=team_stats,
                           team1=team1,
                           team2=team2,
                           team1_name=team1_name,
                           team2_name=team2_name)
