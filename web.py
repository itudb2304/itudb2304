from flask import Flask, render_template
import mysql.connector
import maskPassword as maskPassword

import db_static

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root", 
    password= maskPassword.maskPsw(), 
    database="national_art"  
)

@app.route('/')

def index():
    cur = db.cursor()
    cur.execute("SELECT iiifthumburl FROM published_images")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', images=data)

if __name__ == "__main__":
    db_static.init()
    app.run(debug=True)
