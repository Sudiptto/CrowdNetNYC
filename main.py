from flask import Flask, redirect, render_template, request, jsonify, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
import json
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
    images = {
        'library_icon': url_for('static', filename='library.png'),
        
    }

    
    return render_template('index.html', api_key=api_key, images=images)

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

# SEND DATA FROM THE CSV FILE TO JAVASCRIPT
@app.route('/get_csv_data')
def get_csv_data():
    # Read data from the CSV file
    data = pd.read_csv('NycHotspots.csv')
    #print(data)
    # Convert the data to JSON format
    json_data = data.to_json(orient='records')

    return json.dumps(json_data)

@app.route('/data')  # send the data to the javascript file
def data():
    allData = Location.query.all()
    allInformation = []
    #ADD DATA TO DATABASE TO allInformation
    for i in allData:
        allInformation.append([i.latitude, i.longitude, i.date, i.wifi_username, i.wifi_password]) # append the latitude and longitude values , date, wifi_username and wifi_password, this creates a two dimensional array
    my_list = allInformation
    return jsonify(my_list)


# DELETE DATA

# make a function to delete the location data (Note: Authentication not implemented yet!)
@app.route("/delete_data", methods=["POST"])
def delete_data():
    if request.method == "POST":
        # get the data from JavaScript 
        req = request.get_json()
        new_req = json.loads(req)
        latitude = new_req['lat']
        longitude = new_req['lng']

        lat = float(latitude)
        long = float(longitude)

        latitude_exists = Location.query.filter_by(latitude=lat).first()
        longitude_exists = Location.query.filter_by(longitude=long).first()
        if latitude_exists and longitude_exists:
            print("Latitude and Longitude exists")
            db.session.delete(latitude_exists) # delete whole database
            db.session.commit()
        else:
            print("Non exist")

    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res



# NOTE DATABASE ONLY WORKS BECAUSE WE ARE RUNNING FLASK SQLALCHEMY ON AN OLDER VERSION , 1.4.41
# note not working on linux for some reason 
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)