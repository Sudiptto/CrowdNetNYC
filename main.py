from flask import Flask, redirect, render_template, request, jsonify, make_response
from password import *

app = Flask(__name__)

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
        #city = req['city']
        # Print the extracted values.
        print(f'Latitude: {latitude}, Longitude: {longitude}, Zipcode: {zipcode}') # returns latitude, longitude and ZIPCODE!

    # Note, ALWAYS RETURN JSON DATA BACK OR ELSE YOU WILL HAVE AN ISSUE!
    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res
if __name__ == '__main__':
    app.run(debug=True)