from flask import Flask, render_template, request, redirect, url_for, flash
import emoji
import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
# from flask_caching import Cache



app=Flask(__name__)
       

@app.route('/')
def Index():
    
    return render_template('index.html')
# cursor.execute(sql)
# for row in cursor:
    # do some stuff
    cursor.close()

    #all_flights = Flights.query.all()

   # return render_template('index.html', flights=all_flights)
   #return render_template('index.html')

# Test route
# @ Lennart und Felix: hier könnt ihr euren code einfügen und den server mal testen
@app.route('/cachetest')
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
    
@app.route('/dbtest')  
def dbtest():
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
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Datenbank :poop:', use_aliases=True) 
# test ob der service mit dns erreichbar ist  
@app.route('/servicetest')  
def servicetest():
    try: 
        con = psycopg2.connect("host=10.101.162.210 port=5432 dbname=kranichairline_db user=postgres password=postgres")
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    
    # cursor = conn.cursor()
    # print("test")
    # print(cursor.execute("SELECT * FROM flights"))
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Datenbank :poop:', use_aliases=True) 
# Test ob der Postgres-Pod mit IP erreichbar ist        
@app.route('/podtest')  
def podtest():
    try: 
        con = psycopg2.connect("host=172.17.0.5 port=5432 dbname=kranichairline_db user=postgres password=postgres")
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    
    # cursor = conn.cursor()
    # print("test")
    # print(cursor.execute("SELECT * FROM flights"))
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Datenbank :poop:', use_aliases=True)     

@app.route('/your_flask_funtion')
def your_flask_funtion():
    print("coolio")
    return emoji.emojize('Datenbank :poop:', use_aliases=True)
      
  
  
