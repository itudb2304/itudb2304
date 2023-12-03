from flask import Flask
import mysql.connector
import utils.maskPassword as maskPassword
from utils.path import path
import views
from controllers.constituents_bp import constituents_bp
from controllers.admin_bp import admin_bp
from controllers.locations_bp import locations_bp
from controllers.objects_bp import objects_bp

def create_app():
    app = Flask(__name__ )

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/media", view_func=views.media_page)
    app.add_url_rule("/artwork", view_func=views.artwork_page)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # root in default
        password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
        database="national_art"  #the database created in mySQL and it is in use (mySQL is UP!)
    )

    app.register_blueprint(constituents_bp(connection=connection))
    app.register_blueprint(admin_bp(connection=connection))
    app.register_blueprint(locations_bp(connection=connection))
    app.register_blueprint(objects_bp(connection=connection))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
