from olivier import suggest_airport
from cities import select_best_cities_fixed
from randomWalk import randomWalk

from flask import Flask, request, render_template, jsonify
app = Flask("Skyscanner-CONpagnons")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fromPicture')
def fromPicture():
    return render_template('from-image.html')

@app.route('/goPicture', methods = ['POST'])
def fromPictureURL():
    return jsonify(select_best_cities_fixed(request.form['pictureURL'], 4))

@app.route('/suggestAirport/<needle>')
def suggestAirport(needle):
    return jsonify(suggest_airport(needle))

@app.route('/walk/<depart>/<int:budget>/<from_date>/<to_date>/<int:escale_length>')
def walk(depart, budget, from_date, to_date, escale_length):
    return jsonify(randomWalk(depart, budget, from_date, to_date, dayspercity=escale_length))

