
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

 
 


  
#Mappings    
### Muss angepasst werden
class Flights(db.Model):
    flight_no = db.Column(db.Integer, primary_key = True)
    origin = db.Column(db.String())
    destination = db.Column(db.String())
    seats = db.Column(db.Integer())
    booked_seats = db.Column(db.Integer())
    price = db.Column(db.numeric())
    date = db.Column(db.date())
    

    def __init__(self, origin, destination, seats, booked_seats, price, date):

        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.booked_seats = booked_seats
        self.price = price
        self.date = date
        
#This is the index route where we are going to
#query on all our presence and coronatests data and the contactpersons
@app.route('/')
def Index():
    flights = flights.query.all()


    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM flights"
    cur.execute(s) # Execute the SQL
    list_flights = cur.fetchall()  
 
    return render_template("index.html", presence = all_presence)






 
 
 
if __name__ == "__main__":
    app.run(debug=True, host ="0.0.0.0", port=5000)

