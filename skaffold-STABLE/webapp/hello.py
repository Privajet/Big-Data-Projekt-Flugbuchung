from flask import Flask, render_template, request, redirect, url_for, flash
import emoji
import socket
import psycopg2
from pymemcache.client.base import Client
from essential_generators import DocumentGenerator
from kafka import KafkaProducer
# Lennart, 26.8
# from flask_caching import Cache
client = Client('memcached-service')
app=Flask(__name__)

# Test Zugriff auf den Webserver
@app.route('/')
def Index():
    
    return render_template('index.html')


#   Test Cacheserver, Lennart, 26.08.
#   Die Verbindung zur Datenbank steht bereits.
@app.route('/deployment')
def depl():
    

    ## Datenabfrage aus Cacheserver
    cache_result = client.get('flights')

    ## Wenn keine Daten im Cache, ziehe aus der Datenbank
    if cache_result is None:  #flights nicht verfügbar
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        client.set('flights', data)
        return render_template('index3.html', data=data)
    else: 
#### TODO: Ausgabeformat ist noch nicht schön
        # Wenn verfügbar, nehme die Daten aus dem Cache
        data=cache_result
        return render_template('index3.html', data=data)
    # except Exception as e:
    #     data=e
    #     return emoji.emojize('Cacheserver ist :poop:', use_aliases=True) 

# Funktion zum Senden der Daten an das Kafka-Topic, die bei Klick des Buttons aufgerufen wird
@app.route('/kafka')
def your_flask_funtion():
    # Senden Bei Klick
    producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap:9092')
    next_click = "KLICK GEHT"
#     print(f"Sending message: {next_click}")
    future = producer.send("1337datascience", next_click.encode())
    result = future.get(timeout=5)
#     print(f"Result: {result}")
    return emoji.emojize(':thumbsup:', use_aliases=True) 


###### Entwurf
### Alternativ könnte man eine seite bauen, die solange der user sich darauf befindet nachrichten in das Topic sendet 
# und so das Interesse der Nutzer abschätzen und dementsprechen die Preise erhöhen
@app.route('/zeitbasiert')
def timed_producer():
    producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-bootstrap:9092')

    while True:
        next_msg = "nochda"
        print(f"Sending message: {next_msg}")
        future = producer.send("1337datascience", next_msg.encode())
        result = future.get(timeout=10)
        print(f"Result: {result}")
        time.sleep(5)

############### Ab hier sind alles Testseiten ################
# Test des Datenbankzugriffs

@app.route('/cachetest')
def test():
      ## Datenabfrage aus Cacheserver
    cache_result = client.get('flights')

    ## Wenn keine Daten im Cache, ziehe aus der Datenbank
    if cache_result is None:  #flights nicht verfügbar
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()
        client.set('flights', data)
        return emoji.emojize('Daten waren nicht im Cacheserver :thumbsdown:', use_aliases=True) 
    else: 
        # Wenn verfügbar, nehme die Daten aus dem Cache
        data=cache_result
        return emoji.emojize('Daten waren im Cacheserver :thumbsup:', use_aliases=True) 
    # except Exception as e:
    #     data=e
    #     return emoji.emojize('Cacheserver ist :poop:', use_aliases=True) 

# Test des Datenbankzugriffs
@app.route('/dbtest')  
def dbtest():
    con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
    cur = con.cursor()
    cur.execute("select * from flights")
    data = cur.fetchall()
    cur.close()
    return render_template('index3.html', data=data)
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


# test ob sich die preise ändern lassen
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

# Test ob sich Messages lesen lassen
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

