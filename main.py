from flask import Flask, redirect, render_template, request, jsonify, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
import pandas as pd 
from password import *


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False) # get the values z
    longitude = db.Column(db.Float, nullable=False) # get the valuez
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    zipcode = db.Column(db.Integer, nullable=False) # get the integer
    city = db.Column(db.String, nullable=False)
    wifi_password = db.Column(db.String, nullable=False)
    wifi_username = db.Column(db.String, nullable=False)

# FUNCTIONS (GET CITY)
# NOTE WE GOT THIS DATA THROUGH THE NYC_ZIPCODES CSV FILE, BASED ON THE ZIPCODES!!!
def get_city(zip):
        if zip >= 11201 and zip <= 11256:
            city = 'Brooklyn'
        elif zip >= 11004 and zip<= 11697:
            city = 'Queens'
        elif zip >= 10001 and zip<= 10286:
            city = 'Manhattan'
        elif zip >= 10451 and zip<= 10475:
            city = 'Bronx'
        else:
            city = 'Staten Island'

        return city
    

@app.route('/')
def index():
    return render_template('index.html', api_key=api_key)

# add data into the database
@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        req = request.get_json() # get json data which turns into string
        print(req)
        latitude = req['latitude']
        longitude = req['longitude']
        zipcode = req['zipcode']
        wifiPassword = req['wifiPassword']
        wifiUsername = req['wifiUsername']
        # Print the extracted values.
        #print(f'Latitude: {latitude}, Longitude: {longitude}, Zipcode: {zipcode}, wifiPassword: {wifiPassword}, wifiUsername: {wifiUsername}') # returns latitude, longitude and ZIPCODE!

        # get the city data based on function above:
        city = get_city(int(zipcode))
        #print(city)

        # PUSH TO DATABASE

        pushed_data = Location(latitude=float(latitude), longitude=float(longitude), city=city, zipcode=int(zipcode), wifi_password=wifiPassword, wifi_username=wifiUsername)
        db.session.add(pushed_data)
        db.session.commit() 
        return redirect(url_for('index'))

    # Note, ALWAYS RETURN JSON DATA BACK OR ELSE YOU WILL HAVE AN ISSUE!
    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res

# NOTE DATABASE ONLY WORKS BECAUSE WE ARE RUNNING FLASK SQLALCHEMY ON AN OLDER VERSION , 1.4.41
# note not working on linux for some reason 
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)