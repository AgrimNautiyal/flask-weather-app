import json
import pytz
import requests
from datetime import datetime
import urllib.request
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, flash
from wtforms import Form, TextAreaField, validators
import sqlite3
import urllib.parse
from newsapi import NewsApiClient

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
        url = url.replace(" ", "%20")
        response = urllib.request.urlopen(url).read()
        weather = json.loads(response)
        current_temp = int(weather['main']['temp'])
        current_humidity = weather['main']['temp']
        current_ws = weather['wind']['speed']
        #now to find coords of each of above city and display time zone in the live cameras section
        coords =[]
        for i in def_city:
            url = "http://api.openweathermap.org/data/2.5/weather?q=" +i+"&units=metric&appid=" + str(app.config.get("API_KEY"))
            url = url.replace(" ", "%20")
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
        #now to fill in the news palette for current city
        newsapi = NewsApiClient(api_key=str(app.config.get("NEWS_API")))
        all_articles = newsapi.get_everything(q=current_city, sort_by='relevancy')
        news_content = all_articles['articles'][0:3]


        return render_template('form.html', def_city = def_city, times = times, day = day, date = date, current_city = current_city, current_temp = current_temp, current_humidity = current_humidity, current_ws = current_ws, news_content = news_content)

#WEATHER DISPLAY LOGIC
@app.route('/checkInput', methods = ['POST'])
def display():
    #print('inside the rout!')
    city = request.form['name']
    url = "http://api.openweathermap.org/data/2.5/weather?q=" +city+"&units=metric&appid=" + str(app.config.get("API_KEY"))
    try:

            url = url.replace(" ", "%20")
            print(url)
            response = urllib.request.urlopen(url).read()
            weather = json.loads(response)
            #parsed response to JSON
            temp = int(weather['main']['temp'])
            pressure = weather['main']['pressure']
            humidity = weather['main']['humidity']
            ws = weather['wind']['speed']
            wind_deg = weather['wind']['deg']
            #now to configure the news palette (top 3 new)
            newsapi = NewsApiClient(api_key=str(app.config.get("NEWS_API")))
            all_articles = newsapi.get_everything(q=city, sort_by = 'relevancy')
            news_content = all_articles['articles'][0:3]

            news_title_0 = news_content[0]['title']
            news_title_1 = news_content[1]['title']
            news_title_2 = news_content[2]['title']

            news_desc_0 = news_content[0]['description']
            news_desc_1 = news_content[1]['description']
            news_desc_2 = news_content[2]['description']

            news_url0 = news_content[0]['url']
            news_url1 = news_content[1]['url']
            news_url2 = news_content[2]['url']
            return jsonify({
            'name' : city, 'temp' : temp, 'hum' : str(humidity)+'%', 'ws' : str(ws)+"m/s",
            'news_title_0' : news_title_0, 'news_title_1' : news_title_1, 'news_title_2' : news_title_2,
            'news_content_0' : news_desc_0, 'news_content_1' : news_desc_1, 'news_content_2' : news_desc_2,
            'news_url0' : news_url0, 'news_url1' : news_url1, 'news_url2': news_url2
            })
    except:
            flash('Invalid City. Please try again.')
            return jsonify({'error' : 'Missing data!'})

@app.errorhandler(404)
def not_found(e):
  return render_template("errorpage.html")

if __name__ == '__main__':
    app.run(debug=True)
