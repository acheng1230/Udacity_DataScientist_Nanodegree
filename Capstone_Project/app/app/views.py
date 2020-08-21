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

@app.route("/scores")
def scores():
    """
    NBA Scores Page (Live Scores and Past using Datepicker)
    """
    test_gameid = '0021901318'
    test_date = '08-13-2020'

    games = get_games(test_date)
    return render_template("scores.html",
                           games=games,
                           constants=constants)

@app.route('/standings')
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

# @app.route('/scores', methods=["GET"])
# def scores():
#     if request.method == "GET":
#         date = request.args.get("date")
#
#         games = get_games(date)
#         # return render_template("scores.html",
#         #                        datestring=date)
#
#     else:
#         pass
#
#     return render_template("scores.html",
#                            games=games,
#                            constants=constants,
#                            datestring=date)
