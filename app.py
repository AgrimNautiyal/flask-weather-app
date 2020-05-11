import json
import pytz
import requests
from datetime import datetime
import urllib.request
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from wtforms import Form, TextAreaField, validators
import sqlite3

load_dotenv('.env')
app = Flask(__name__)
app.config.from_pyfile('settings.py')
#HOME PAGE
@app.route('/')
def home():
        #display current day and date
        currentDT = datetime.now()
        day = currentDT.strftime("%a")
        date = currentDT.strftime("%b %d")
        #to keep some default cities in the first page
        def_city =  ['New York', 'Delhi', 'Chennai', 'London']

        #to work on extracting current location of user

        current_city = 'Delhi'
        url = "http://api.openweathermap.org/data/2.5/weather?q=" +current_city+"&units=metric&appid=" + str(app.config.get("API_KEY"))
        response = urllib.request.urlopen(url).read()
        weather = json.loads(response)
        current_temp = weather['main']['temp']
        current_humidity = weather['main']['temp']
        current_ws = weather['wind']['speed']
        #now to find coords of each of above city and display time zone in the live cameras section
        coords =[]
        for i in def_city:
            url = "http://api.openweathermap.org/data/2.5/weather?q=" +i+"&units=metric&appid=" + str(app.config.get("API_KEY"))
            response = urllib.request.urlopen(url).read()
            weather = json.loads(response)
            coord = [weather['coord']['lon'], weather['coord']['lat']]
            coords.append(coord)
        #now we have coordinates of each city, so we need to get timezone ID
        timezones=[]
        tf = TimezoneFinder()
        for i in coords:
            timezones.append(tf.timezone_at(lng=i[0], lat=i[1]))
        #now to extract local time in each timezone
        times = []
        for i in timezones:
            location = i
            timezone = pytz.timezone(location)
            time = datetime.now(timezone)
            times.append(time .strftime("%I:%M %p"))
        return render_template('form.html', def_city = def_city, times = times, day = day, date = date, current_city = current_city, current_temp = current_temp, current_humidity = current_humidity, current_ws = current_ws)

#WEATHER DISPLAY LOGIC
@app.route('/checkInput', methods = ['POST'])
def display():
    print('inside the rout!')
    city = request.form['name']
    url = "http://api.openweathermap.org/data/2.5/weather?q=" +city+"&units=metric&appid=" + str(app.config.get("API_KEY"))
    try:
            #tested, environment variables are working as predicted
            response = urllib.request.urlopen(url).read()
            weather = json.loads(response)
            #parsed response to JSON
            temp = weather['main']['temp']
            pressure = weather['main']['pressure']
            humidity = weather['main']['humidity']
            ws = weather['wind']['speed']
            wind_deg = weather['wind']['deg']
            print(weather)
            #return jsonify({'city' : city, 'temp' : temp, 'humidity' : humidity, 'pressure' : pressure, 'wind_speed' : ws, 'wind_direction' : wind_deg})
            return jsonify({'name' : city, 'temp' : temp})
    except:
            return jsonify({'error' : 'Missing data!'})

@app.errorhandler(404)
def not_found(e):
  return render_template("errorpage.html")

if __name__ == '__main__':
    app.run(debug=True)
