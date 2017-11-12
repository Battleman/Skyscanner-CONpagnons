from olivier import suggest_airport
from cities import get_most_likely_cities_file
from randomWalk import randomWalk
from newgetters import fast_getter, heavy_getter

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
    return jsonify(get_most_likely_cities_file(request.form['pictureURL'], 5))

@app.route('/suggestAirport/<needle>')
def suggestAirport(needle):
    return jsonify(suggest_airport(needle))

@app.route('/walk/<depart>/<int:budget>/<from_date>/<int:escale_length>')
def walk(depart, budget, from_date, escale_length):
    while True:
        travel = fast_getter(depart, budget, from_date, dayspercity=escale_length, marge=0.05)
        if len(travel) > 0:
            break

    return jsonify(travel)

@app.route('/heavyWalk', methods=['POST'])
def heavy():
    print(request.data)
    return jsonify(heavy_getter(request.get_json(force=True)))
