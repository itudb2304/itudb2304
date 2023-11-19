from flask import Flask
import mysql.connector
import utils.maskPassword as maskPassword
from utils.path import path
from database import Database
import views

# Your database configuration
# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # root in default
    password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
    database="national_art"  #the database created in mySQL and it is in use (mySQL is UP!)
)

def create_app():
    app = Flask(__name__ )

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/locations", view_func=views.locations_page)
    app.add_url_rule("/locations/location", view_func=views.location_page)
    app.add_url_rule("/admin", view_func=views.admin_page)
    app.add_url_rule("/admin/table", view_func=views.table_page)

    db = Database(password=maskPassword.maskPsw())
    app.config["db"] = db
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
