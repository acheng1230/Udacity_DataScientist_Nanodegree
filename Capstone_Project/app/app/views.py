from app import app
from flask import render_template

from nbapy.scoreboard import Scoreboard
from wrangling_scripts.constants import CITY_TO_TEAM
from wrangling_scripts.wrangle_data import get_games

test_gameid = '0021901318'
test_date = '08-13-2020'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores")
def scores():
    games = get_games(test_date)

    winners = []
    for i, value in games.iterrows():
        if (value["HOME_TEAM_PTS"] > value["VISITOR_TEAM_PTS"]):
            winners.append(value["HOME_TEAM_ABBREVIATION"])
        elif (value["HOME_TEAM_PTS"] < value["VISITOR_TEAM_PTS"]):
            winners.append(value["VISITOR_TEAM_ABBREVIATION"])
        else:
            winners.append(None)

    return render_template("scores.html",
                           games=games,
                           winners=winners)

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
                           west_standings=west_standings,
                           team=CITY_TO_TEAM)
