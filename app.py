from flask import Flask
import mysql.connector
import maskPassword as maskPassword
from path import path
import db_static

app = Flask(__name__ )

# Your database configuration
# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # root in default
    password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
    database="national_art"  #the database created in mySQL and it is in use (mySQL is UP!)
)

@app.route("/")
def table_names():
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    rv = cursor.fetchall()
    table_names = [row[0] for row in rv]
    return "<br>".join(table_names)

if __name__ == "__main__":
    db_static.init()
    app.run(debug=True)
