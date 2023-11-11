import mysql.connector
import maskPassword

db = mysql.connector.connect(
    host="localhost",
    user="root",  # root in default
    password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
    database="national_art",  #the database created in mySQL and it is in use (mySQL is UP!)
    allow_local_infile=True
)

cursor = db.cursor()
path = 'C:/Users/hacer/Desktop/csv/' # the path of data set folder 

def init():
    query = ''' CREATE TABLE IF NOT EXISTS preferred_locations(    
        locationkey VARCHAR(30),
        locationtype VARCHAR(15),
        description VARCHAR(100),
        ispublicvenue INTEGER,
        mapshapetype VARCHAR(10),
        mapshapecoords VARCHAR(100),
        partof VARCHAR(100),
        PRIMARY KEY (locationkey)
    );'''
    cursor.execute(query)
    db.commit()
    
    query = f''' LOAD DATA LOCAL INFILE '{path}preferred_locations.csv'
    INTO TABLE preferred_locations
    FIELDS TERMINATED BY ','
    IGNORE 1 ROWS;'''
    cursor.execute(query)
    db.commit()

    query = '''UPDATE preferred_locations
    SET description = REPLACE(description, '/', ','); 
    '''
    cursor.execute(query)
    db.commit()

    query = ''' CREATE TABLE IF NOT EXISTS locations(    
        locationid INTEGER,
        site VARCHAR(30),
        room VARCHAR(10),
        publicaccess INTEGER,
        description VARCHAR(50),
        unitposition VARCHAR(20),
        mapimageurl VARCHAR(100),
        PRIMARY KEY (locationid),
        FOREIGN KEY (room) REFERENCES preferred_locations(locationkey) ON DELETE CASCADE ON UPDATE CASCADE
    );
    '''
    cursor.execute(query)
    db.commit()
    
    query = f''' 
    LOAD DATA LOCAL INFILE '{path}locations.csv'
    INTO TABLE locations
    FIELDS TERMINATED BY ','
    IGNORE 1 ROWS;'''
    cursor.execute(query)
    db.commit()

    query = '''    UPDATE locations
    SET description = REPLACE(description, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

init()