from flask import render_template,request,flash,redirect,url_for
from twitter_trends import app
from twitter_trends.utility import convert_to_excel
import requests,os
import tweepy
import geocoder
import json


auth = tweepy.OAuthHandler("sex29TpI3XrfIwFMr13PZCbJm", "WDIbuVJMZCe4PULV8oKts43HHnjiwDp66DzeHILZLFztMnkCLI")
auth.set_access_token("2226801236-7s0f4keOyp0kxxf0l9VYc5UgGSdHCdP2lK4CIBT", "yfKMwFZQOda6MPEtcIx3A4GDPCfs8BEvSzsocHDWq57mz")
api_obj = tweepy.API(auth)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data", "locations.json")
data = json.load(open(json_url))
sorted_data = sorted(data.items(),key= lambda x:x[0])

@app.route("/")
def index():
    trends = api_obj.get_place_trends(1)
    trends = trends[0]['trends']
    excel_data = convert_to_excel(trends)
    
    return render_template("index.html",data=trends,excel_data=excel_data,location_list = sorted_data,country=False,city=False)


@app.route("/",methods=['POST','GET'])
def manage_location():
    if request.method == "POST":
        return redirect(url_for('location_specific',location=request.form['location']))


@app.route("/<string:location>",methods=['POST','GET'])
def country_specific(location):
    for i in data:
        if i==location:
            id = data[i][0]
            break

    trends = api_obj.get_place_trends(id)
    trends = trends[0]['trends']
    excel_data = convert_to_excel(trends)

    return render_template("index.html",data=trends,excel_data=excel_data,location_list = sorted_data,country=location,city=False)

@app.route("/<string:country>/<string:city>")
def city_specific(country,city):
    for i in data:
        if i==country:
            for j in data[i][2]['cities']:
                if j[0]==city:
                    id = j[1]
                    break

    trends = api_obj.get_place_trends(id)
    trends = trends[0]['trends']
    excel_data = convert_to_excel(trends)
    return render_template("index.html",data=trends,excel_data=excel_data,location_list = sorted_data,city=city,country=country)
