from app import app
from flask import render_template

from wrangling_scripts.wrangle_data import get_games

test_gameid = '0021901318'
test_date = '08-13-2020'

@app.route("/")
def index():
    games = get_games(test_date)
    games
    return render_template("index.html", data_set=games)

@app.route("/about")
def about():
    return "<h1 style='color:red'>About!!!</h1>"
