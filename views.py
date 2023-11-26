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
    cur.execute("SELECT iiifthumburl FROM published_images LIMIT 500")
    data = cur.fetchall()
    cur.close()

    return render_template('media.html', images=data)


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

def admin_page():
    db = current_app.config["db"]
    table_names = db.get_table_names()
    if table_names is None:
        abort(404)
    else:
        return render_template("admin.html", table_names=table_names)
    
def constituents_page():
    db = current_app.config["db"]
    constituents = db.get_all_constituents()
    if constituents is None:
        abort(404)
    else:
        return render_template("constituents.html", constituents=constituents)

def table_page(table_name):
    db = current_app.config["db"]
    table_headers, table_content = db.get_table_content(table_name)
    if table_content is None:
        abort(404)
    else:
        return render_template("table.html", table_headers=table_headers, table_content=table_content)
