import mysql.connector
import utils.maskPassword as maskPassword
from utils.path import path

db = mysql.connector.connect(
    host="localhost",
    user="root",  # root in default
    password= maskPassword.maskPsw(), # your mySQL password written in maskPassword.py file!
    database="national_art",  #the database created in mySQL and it is in use (mySQL is UP!)
    allow_local_infile=True
)

cursor = db.cursor()

def init():
    query = ''' 
        CREATE TABLE IF NOT EXISTS preferred_locations(    
        locationkey VARCHAR(30),
        locationtype VARCHAR(15),
        description VARCHAR(100),
        ispublicvenue INTEGER,
        mapshapetype VARCHAR(10),
        mapshapecoords VARCHAR(100),
        partof VARCHAR(100),
        PRIMARY KEY (locationkey)
    );
    '''
    cursor.execute(query)
    db.commit()
    
    query = f''' 
        LOAD DATA LOCAL INFILE '{path}preferred_locations.csv'
        INTO TABLE preferred_locations
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE preferred_locations
        SET mapshapecoords = REPLACE(mapshapecoords, '/', ','); 
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        CREATE TABLE IF NOT EXISTS locations(    
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
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE locations
        SET description = REPLACE(description, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = '''
        CREATE TABLE IF NOT EXISTS constituents(
        constituentid INTEGER,
        ulanid VARCHAR(32),
        preferreddisplayname VARCHAR(256),
        forwarddisplayname VARCHAR(256),
        lastname VARCHAR(256),
        displaydate VARCHAR(256),
        artistofngaobject INTEGER,
        beginyear INTEGER,
        endyear INTEGER,
        visualbrowsertimespan VARCHAR(32),
        nationality VARCHAR(128),
        visualbrowsernationality VARCHAR(128),
        constituenttype VARCHAR(30),
        wikidataid VARCHAR(64),
        PRIMARY KEY (constituentid)
    );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}constituents.csv'
        INTO TABLE constituents
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE constituents
        SET preferreddisplayname = REPLACE(preferreddisplayname, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE constituents
        SET displaydate = REPLACE(displaydate, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = '''
        CREATE TABLE IF NOT EXISTS objects (
        objectid                    INT,
        accessioned                 INT,
        accessionnum                VARCHAR(32),
        locationid                  INT,
        title                       TEXT,
        displayDate                 VARCHAR(256),
        beginYear                   INT,
        endYear                     INT,
        visualBrowserTimeSpan       VARCHAR(32),
        medium                      TEXT,
        dimensions                  TEXT,
        inscription                 VARCHAR(255),
        markings                    VARCHAR(255),
        attributionInverted         VARCHAR(1024),
        attribution                 VARCHAR(1024),
        provenanceText              TEXT,
        creditLine                  TEXT,
        classification              VARCHAR(64),
        subClassification           VARCHAR(64),
        visualBrowserClassification VARCHAR(32),
        parentid                    INT,
        isVirtual                   INT,
        departmentabbr              VARCHAR(32),
        portfolio                   TEXT,
        series                      VARCHAR(850),
        volume                      VARCHAR(850),
        watermarks                  VARCHAR(512),
        lastDetectedModification    TIME,
        wikidataid                  VARCHAR(64),
        customPrintURL              TEXT,
        PRIMARY KEY(objectid),
        FOREIGN KEY(locationid) references locations(locationid) ON DELETE CASCADE ON UPDATE CASCADE
        ); 
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}objects.csv'
        INTO TABLE objects
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET attributioninverted = REPLACE(attributioninverted, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET attribution = REPLACE(attribution, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET inscription = REPLACE(inscription, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET provenancetext = REPLACE(provenancetext, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET title = REPLACE(title, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET creditline = REPLACE(creditline, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET displaydate = REPLACE(displaydate, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET medium = REPLACE(medium, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET dimensions = REPLACE(dimensions, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET markings = REPLACE(markings, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET subclassification = REPLACE(subclassification, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET portfolio = REPLACE(portfolio, '/', ','); 
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET series = REPLACE(series, '/', ','); 
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET volume = REPLACE(volume, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects
        SET watermarks = REPLACE(watermarks, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}media_relationships.csv'
        INTO TABLE media_relationships
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        CREATE TABLE IF NOT EXISTS published_images(    
        uuid VARCHAR(50),
        iiifurl VARCHAR(100),
        iiifthumburl VARCHAR(100),
        viewtype VARCHAR(20),
        sequence INTEGER,
        width INTEGER,
        height INTEGER,
        maxpixels INTEGER,
        created VARCHAR(10),
        modified VARCHAR(10),
        depictstmsobjectid INTEGER,
        assistivetext VARCHAR(500),
        PRIMARY KEY (uuid)
    );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}published_images.csv'
        INTO TABLE published_images
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        UPDATE published_images
        SET iiifthumburl = CONCAT(iiifthumburl, ',200/0/default.jpg')

    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        UPDATE published_images
        SET iiifthumburl = TRIM('"' FROM iiifthumburl);

    '''
    cursor.execute(query)
    db.commit()

    
    query = ''' 
        CREATE TABLE IF NOT EXISTS media_items(    
        mediaid INTEGER,
        mediatype VARCHAR(10),
        title VARCHAR(50),
        description VARCHAR(500),
        duration VARCHAR(100),
        language VARCHAR(10),
        thumbnailurl VARCHAR(256),
        playurl VARCHAR(256),
        downloadurl VARCHAR(256),
        keywords VARCHAR(256),
        tags VARCHAR(256),
        imageurl VARCHAR(256),
        presentationdate VARCHAR(30),
        releasedate VARCHAR(30),
        lastmodified VARCHAR(30),
        PRIMARY KEY (mediaid)
    );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}media_items.csv'
        INTO TABLE object_media
        FIELDS TERMINATED BY '\t'
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        CREATE TABLE IF NOT EXISTS object_media(    
        mediaid INTEGER,
        mediatype VARCHAR(10),
        title VARCHAR(50),
        description VARCHAR(500),
        duration VARCHAR(100),
        language VARCHAR(10),
        thumbnailurl VARCHAR(256),
        playurl VARCHAR(256),
        downloadurl VARCHAR(256),
        keywords VARCHAR(256),
        tags VARCHAR(256),
        imageurl VARCHAR(256),
        presentationdate VARCHAR(30),
        releasedate VARCHAR(30),
        lastmodified VARCHAR(30),
        PRIMARY KEY (mediaid)
    );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}object_media.csv'
        INTO TABLE object_media
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()



    query = ''' 
        CREATE TABLE IF NOT EXISTS constituents_media(    
        mediaid INTEGER,
        mediatype VARCHAR(10),
        title VARCHAR(50),
        description VARCHAR(500),
        duration INTEGER,
        language VARCHAR(10),
        thumbnailurl VARCHAR(256),
        playurl VARCHAR(256),
        downloadurl VARCHAR(256),
        keywords VARCHAR(256),
        tags VARCHAR(256),
        imageurl VARCHAR(256),
        presentationdate VARCHAR(30),
        releasedate VARCHAR(30),
        lastmodified VARCHAR(30),
        PRIMARY KEY (mediaid)
    );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}constituents_media.csv'
        INTO TABLE constituents_media
        FIELDS TERMINATED BY ','
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = '''
        CREATE TABLE IF NOT EXISTS objects_historical_data (
            dataType VARCHAR(32) NOT NULL,
            objectID INTEGER,
            displayOrder INTEGER NOT NULL,
            forwardText VARCHAR(256),
            invertedText VARCHAR(256),
            remarks VARCHAR(256),
            effectiveDate VARCHAR(10),
            FOREIGN KEY (objectID) REFERENCES objects(objectid) ON DELETE CASCADE ON UPDATE CASCADE
        );
    '''
    cursor.execute(query)
    db.commit()

    query = f'''
        LOAD DATA LOCAL INFILE '{path}objects_historical_data.csv'
        INTO TABLE objects_historical_data
        FIELDS TERMINATED BY ';'
        IGNORE 1 ROWS;
    '''
    cursor.execute(query)
    db.commit()

    query = ''' 
        UPDATE objects_historical_data
        SET invertedText = REPLACE(invertedText, '/', ',');
    '''
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()

init()
