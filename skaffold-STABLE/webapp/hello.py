from flask import Flask, render_template, request, redirect, url_for, flash
import emoji
import socket
import psycopg2
#from pymemcache.client import base
from pymemcache.client.base import Client
#import time
from essential_generators import DocumentGenerator
from kafka import KafkaProducer
# Lennart, 26.8
# from flask_caching import Cache
client = Client('memcached-service')

app=Flask(__name__)
# cache = Cache()


# Test Zugriff auf den Webserver
@app.route('/')
def Index():
    
    return render_template('index.html')


#   Test Cacheserver, Lennart, 26.08.
#   Die Verbindung zur Datenbank steht bereits.
@app.route('/cachetest')
def test():
    cache_result = client.get('flights')

    if cache_result is None:  #flights nicht verfügbar
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        client.set('flights', data)
        return emoji.emojize('Cacheeintrag :poop:', use_aliases=True) 
    else: 
        return emoji.emojize('Cacheserver geht :thums_up:', use_aliases=True) 


    try: 
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Cacheserver ist :poop:', use_aliases=True) 

# Test des Datenbankzugriffs
@app.route('/dbtest')  
def dbtest():
    try: 
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        print('+=========================+')
        print('|  CONNECTED TO DATABASE  |')
        print('+=========================+')
    
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Datenbank :poop:', use_aliases=True) 
# Test ob der service mit DNS erreichbar ist - aktuelle IP einfügen
# UPDATE 24.08.
# Fehler bei der DNS-Erreichbarkeit lag an "k delete --all --all-namespaces", was auch den DNS-Pod löscht
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
# Test ob der Postgres-Pod mit IP erreichbar ist, aktuelle IP einfügen     
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

# Funktion zum Senden der Daten an das Kafka-Topic, die bei Klick des Buttons aufgerufen wird
@app.route('/kafka')
def your_flask_funtion():
    
    # Vorlage aus Vorlesungs-Skript

    #gen = DocumentGenerator()

    producer = KafkaProducer(
    bootstrap_servers='my-cluster-kafka-kafka11-bootstrap:29092')

    next_click = "ein Klick passiert"
#     print(f"Sending message: {next_click}")
    future = producer.send("1337datascience", next_click)
    result = future.get(timeout=5)
#     print(f"Result: {result}")
    return result

## Hier noch die Abfrage richtig machen dass auch gespeichert wird. So erhöht er zwar die Preise aber die DB-Einträge werden 
# irgendwie nicht geändert

@app.route('/changedb')  
def changetest():
    try: 
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("UPDATE flights SET price= price + (price * 10 / 100) ")
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        return render_template('index3.html', data=data)
    except Exception as e:
        data=e
        return emoji.emojize('Datenbank-Schreiben :poop:', use_aliases=True)      
  
@app.route('/kafkaread')  

def kafkaread():
    
    from kafka import KafkaConsumer
    # The bootstrap server to connect to
    bootstrap = 'my-cluster-kafka-kafka-bootstrap:9092'
    # Create a comsumer instance
    # cf.
    print('Starting KafkaConsumer')
    consumer = KafkaConsumer('1337datascience', # <-- topics
    bootstrap_servers=bootstrap)
    # Print out all received messages
    data=[]
    for msg in consumer:
        data.append(msg)
    return render_template('index3.html', data=data)


@app.route('/kafkaread2')  

def kafkaread2():
    
    from kafka import KafkaConsumer
    # The bootstrap server to connect to
    bootstrap = 'my-cluster-kafka-kafka-bootstrap:9092'
    # Create a comsumer instance
    # cf.
    print('Starting KafkaConsumer')
    consumer = KafkaConsumer('1337datascience', # <-- topics
    bootstrap_servers=bootstrap)
    # Print out all received messages
    data=[]
    for msg in consumer:
        data.append(msg)
    return data

