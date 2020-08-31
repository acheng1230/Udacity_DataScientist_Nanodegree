from app import app
from flask import render_template, request, redirect, abort

import feedparser
import dateutil.parser
import datetime, json, plotly
from nbapy.scoreboard import Scoreboard
from wrangling_scripts import constants
from wrangling_scripts.wrangle_data import *

# A function that forces recaching every 10 minutes.
@app.after_request
def add_header(response):
    # Add headers to both force latest IE rendering engine or Chrome Frame,
    # and also to cache the rendered page for 10 minutes.
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Routes for Pages
@app.route("/")
def index():
    feed_url = "https://www.espn.com/espn/rss/nba/news"
    feed = feedparser.parse(feed_url)

    titles = []
    links = []
    for article in feed['entries'][:7]:
        titles.append(article['title'])
        links.append(article['links'][0]['href'])

    news = zip(titles, links)
    return render_template("public/index.html",
                           news=news)

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

    return render_template("public/scores.html",
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

    return render_template("public/standings.html",
                           east_standings=east_standings,
                           west_standings=west_standings)

@app.route("/boxscores/<gameid>")
def boxscores(gameid):
    """
    NBA Box Scores Page (Team Stats, Four Factors, Box Scores and Highlights)
    """
    # Box Scores
    team1, team2, summary = get_boxscore(gameid)
    team1_id = str(team1['TEAM_ID'].unique()[0])
    team1_name = constants.TEAM_ID_TO_NAME[team1_id]['team-name']
    team1_abbrev = constants.TEAM_ID_TO_NAME[team1_id]['abbrev']

    team2_id = str(team2['TEAM_ID'].unique()[0])
    team2_name = constants.TEAM_ID_TO_NAME[team2_id]['team-name']
    team2_abbrev = constants.TEAM_ID_TO_NAME[team2_id]['abbrev']

    # Data Visualizations
    bar1, bar2 = create_teamstats_barchart(gameid)
    pct_bar1, pct_bar2 = create_teampct_barchart(gameid)

    return render_template("public/boxscores.html",
                           constants=constants,
                           team1=team1,
                           team2=team2,
                           team1_name=team1_name,
                           team2_name=team2_name,
                           team1_abbrev=team1_abbrev,
                           team2_abbrev=team2_abbrev,
                           summary=summary,
                           bar1=bar1,
                           bar2=bar2,
                           pct_bar1=pct_bar1,
                           pct_bar2=pct_bar2)

@app.route("/about")
def about():
    return render_template("public/about.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("error/404.html"), 404

@app.errorhandler(500)
def server_error(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("error/500.html"), 500

    # wrapped unhandled error
    return render_template("error/500.html", e=original), 500


"""
Test Workspace
"""
@app.route("/test")
def test():
    return render_template("test/test.html")
