
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

 

 
app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration 
##### Hier URL ANPASSEN ###
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgres',url='localhost',db='kranichairline_db')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

conn_string = "host="+"localhost"+" port="+"5432"+" dbname="+"kranichairline_db"+ \
    " user="+"postgres" + " password="+"postgres"
conn=psycopg2.connect(conn_string)

db = SQLAlchemy(app)


 
#Mappings    
### Muss angepasst werden
class Presence(db.Model):
    ID = db.Column(db.Integer, primary_key = True)
    chip_no = db.Column(db.Integer())
    room_no = db.Column(db.Integer())
    date = db.Column(db.Integer())
    time_checkin = db.Column(db.Integer())
    time_checkout = db.Column(db.Integer())
    

    def __init__(self, chip_no, room_no,date, time_checkin, time_checkout):

        self.chip_no = chip_no
        self.room_no = room_no
        self.date = date
        self.time_checkin = time_checkin
        self.time_checkout = time_checkout
        
    def __init__(self, pers_no, test_date, positive):

        self.pers_no = pers_no
        self.test_date = test_date
        self.positive = positive

#This is the index route where we are going to
#query on all our presence and coronatests data and the contactpersons
@app.route('/')
def Index():
    all_presence = Presence.query.all()
    all_tests = Corona_tests.query.all()

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM contactpersons"
    cur.execute(s) # Execute the SQL
    list_contactpersons = cur.fetchall()  
 
    return render_template("index.html", presence = all_presence, contactpersons=list_contactpersons, corona_tests=all_tests)






 
 
 
if __name__ == "__main__":
    app.run(debug=True, host ="0.0.0.0", port=5000)

