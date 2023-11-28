from flask import Flask, abort, render_template, current_app, request
import mysql.connector
import utils.maskPassword as maskPassword
import urllib.parse

db = mysql.connector.connect(
    host="localhost",
    user="root", 
    password= maskPassword.maskPsw(), 
    database="national_art"  
)


def media_page():
    cur = db.cursor()
    cur.execute("SELECT thumbnailurl FROM object_media LIMIT 500")
    data = cur.fetchall()
    cur.close()

    return render_template('media.html', images=data)

def artwork_page():
    cur = db.cursor()
    cur.execute("SELECT iiifthumburl, modified, height, maxpixels FROM published_images LIMIT 500")
    data = cur.fetchall()
    cur.close()

    # Extract images and text into separate lists
    images = [row[0] for row in data]
    text = [row[1] for row in data]
    width = [row[2] for row in data]
    height = [row[3] for row in data]

    return render_template('artwork.html', images=images, text=text, width = width, height = height)



def home_page():
    return render_template("home.html")

def location_page(location_key):
    db = current_app.config["db"]
    location = db.get_building(location_key)

    if location is None:
        abort(404)
    else:
        return render_template("location.html", location=location )

def locations_page():
    db = current_app.config["db"]
    locations = db.get_all_buildings()

    if locations is None:
        abort(404)
    else:
        return render_template("locations.html", locations=sorted(locations))

