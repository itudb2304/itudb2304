from flask import Flask
import mysql.connector
import utils.maskPassword as maskPassword
from utils.path import path
from repository.database import Database
import views
from controllers.constituents_bp import constituents_bp

def create_app():
    app = Flask(__name__ )

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/locations", view_func=views.locations_page)
    app.add_url_rule("/locations/location", view_func=views.location_page)
    app.add_url_rule("/admin", view_func=views.admin_page)
    app.add_url_rule("/admin/<string:table_name>", view_func=views.table_page)
    app.add_url_rule("/media", view_func=views.media_page)
    app.add_url_rule("/artwork", view_func=views.artwork_page)

    db = Database(password=maskPassword.maskPsw())
    app.config["db"] = db

    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # root in default
        password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
        database="national_art"  #the database created in mySQL and it is in use (mySQL is UP!)
    )

    app.register_blueprint(constituents_bp(connection=connection))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
