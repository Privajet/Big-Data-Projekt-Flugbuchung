#author: Aniket Mukherjee
from flask import Flask, render_template, request, redirect, url_for, flash
import emoji
import pyjokes
import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
# from flask_caching import Cache
# import psycopg2
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import ForeignKeyConstraint, ForeignKey
# from sqlalchemy.orm import relationship, backref

app=Flask(__name__)


# conn = psycopg2.connect("host=172.17.0.3  port=5432 dbname=kranichairline_db user=postgres password=postgres")
# cursor = conn.cursor()
# print("test")
# print(cursor.execute("SELECT * FROM flights"))

# # cursor.execute(sql)
# # for row in cursor:
    # # do some stuff
# cursor.close()



# app.secret_key = "Secret Key"
 
# #SqlAlchemy Datenbank-Konfiguration
# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgres',url='10.107.191.109:5002',db='kranichairline_db')

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

# db = SQLAlchemy(app)

 ### Datentypen überprüfen
#class Flights(db.Model):
    # flight_no = db.Column(db.Integer, primary_key = True)
    # origin = db.Column(db.Integer())
    # destination = db.Column(db.Integer())
    # seats = db.Column(db.Integer())
    # booked_seats = db.Column(db.Integer())
    # price = db.Column(db.Integer())
    

    # def __init__(self, flight_no, origin, destination, seats, booked_seats, price):

        # self.flight_no = flight_no
        # self.origin = origin
        # self.destination = destination
        # self.seats = seats
        # self.booked_seats = booked_seats
        # self.price = price
        

@app.route('/')
def Index():
    try: 
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    
    # cursor = conn.cursor()
    # print("test")
    # print(cursor.execute("SELECT * FROM flights"))
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
    except Exception as e:
        data=e
    cur = con.cursor()
    cur.execute("select * from flights")
    data = cur.fetchall()
   
    
    # df = pd.DataFrame(data, columns=["Customer ID","First Name","origin","origin","origin","price"])
    # html = df.to_html(index=False)
    cur.close()
    #return '<div id=table> <center>'+data+'<a href="/">Home</a></center> </div>'
    return render_template('index.html', data=data)
# cursor.execute(sql)
# for row in cursor:
    # do some stuff
    cursor.close()

    #all_flights = Flights.query.all()

   # return render_template('index.html', flights=all_flights)
   #return render_template('index.html')

## Test route
# @ Lennart und Felix: hier könnt ihr euren code einfügen und den server mal testen
@app.route('/test')
def test():
    config = {
        "DEBUG": True,          # some Flask specific configs
        "CACHE_TYPE": "MemcachedCache",  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_MEMCACHED_SERVERS":"memcached",
    }

    app.config.from_mapping(config)
    cache = Cache(app)
    return emoji.emojize('Python development with Skaffold is :thumbs_up:')
  
