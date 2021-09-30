# import necessary libraries
from models import create_classes
from models import create_classes2
import os
import json
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Pet = create_classes(db)
Large = create_classes2(db)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        pet = Pet(name=name, lat=lat, lon=lon)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/pals")
def pals():
    results = db.session.query(Pet.name, Pet.lat, Pet.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]

    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]

    return jsonify(pet_data)

@app.route("/api/json")
def json_sample():
    with open('static/data/country-by-languages.json', 'r') as outfile:
        data = json.load(outfile)
    return jsonify(data)

@app.route("/api/csv")
def csv_sample():
    df = pd.read_csv("static/data/abcnews-date-text.csv")
    df = df.iloc[0:50000]
    data = json.loads(df.to_json(orient='records'))
    return jsonify(data)

@app.route("/api/large_dataset")
def large_dataset():
    data = []
    results = db.session.query(Large.name, Large.lat, Large.lon).all()
    for result in results:
        name = result[0]
        lat = result[1]
        lon = result[2]
        data += [{
            "lat": lat,
            "lon": lon,
            "name": name
        }]

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False)
