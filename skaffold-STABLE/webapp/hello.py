from flask import Flask, render_template, request, redirect, url_for, flash
import emoji
import socket
import psycopg2
# from flask_caching import Cache

app=Flask(__name__)
       
# Test Zugriff auf den Webserver
@app.route('/')
def Index():
    
    return render_template('index.html')


# Test Cacheserver
# @ Lennart und Felix: hier könnt ihr euren code einfügen und den server mal testen
#   Die Verbindung zur Datenbank steht bereits.
@app.route('/cachetest')
def test():
    # habe das hier gefunden, vielleicht könnt ihr das verwenden
    # config = {
    #     "DEBUG": True,          # some Flask specific configs
    #     "CACHE_TYPE": "MemcachedCache",  # Flask-Caching related configs
    #     "CACHE_DEFAULT_TIMEOUT": 300,
    #     "CACHE_MEMCACHED_SERVERS":"memcached",
    # }

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
@app.route('/your_flask_funtion')
def your_flask_funtion():
    
    # Vorlage aus Vorlesungs-Skript

    # import time
    # from essential_generators import DocumentGenerator
    # from kafka import KafkaProducer

    # gen = DocumentGenerator()

    # producer = KafkaProducer(
    #     bootstrap_servers='my-cluster-kafka-bootstrap:9092')

    # while True:
    #     next_msg = gen.sentence()
    #     print(f"Sending message: {next_msg}")
    #     future = producer.send("big_data_demo", next_msg.encode())
    #     result = future.get(timeout=5)
    #     print(f"Result: {result}")
    #     time.sleep(2)

    print("coolio")
    return emoji.emojize('Datenbank :poop:', use_aliases=True)

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
  
