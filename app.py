from olivier import suggest_airport
from randomWalk import randomWalk

from flask import Flask, render_template, jsonify
app = Flask("Skyscanner-CONpagnons")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggestAirport/<needle>')
def suggestAirport(needle):
    return jsonify(suggest_airport(needle))

@app.route('/walk/<depart>/<int:budget>/<date>')
def walk(depart, budget, date):
    return jsonify(randomWalk(depart, budget, date))
