
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

 

 
app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration 
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgres',url='localhost',db='ccmgmtdb')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

conn_string = "host="+"localhost"+" port="+"5432"+" dbname="+"ccmgmtdb"+ \
    " user="+"postgres" + " password="+"postgres"
conn=psycopg2.connect(conn_string)

db = SQLAlchemy(app)


 
#Mappings of Presence Table and Corona_tests table    
 
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

class Corona_tests(db.Model):
    pers_no = db.Column(db.Integer, primary_key = True)
    test_date = db.Column(db.Integer())
    id = db.Column(db.Integer, primary_key=True)
    positive = db.Column(db.String())
    
    

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



#This is our insert route where we are going to add an entry in presence
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        chip_no = request.form['chip_no']
        room_no = request.form['room_no']
        date = request.form['date']
        time_checkin=request.form['time_checkin']
        time_checkout=request.form['time_checkout']
 
        my_presence = Presence( chip_no, room_no, date, time_checkin, time_checkout)
        db.session.add(my_presence)
        db.session.commit()
 
        flash("Presence Inserted Successfully")
 
        return redirect(url_for('Index'))


#This is our insert1 route where we are going to add an entry in coronatests
@app.route('/insert1', methods =['Post'])  
def insert1():

    if request.method == 'POST':
 
        pers_no = request.form['pers_no']
        test_date = request.form['test_date']
        positive=request.form['positive']
 
        my_coronatest = Corona_tests( pers_no, test_date, positive)
        db.session.add(my_coronatest)
        db.session.commit()
 
        flash("Test Result Inserted Successfully")
        return redirect(url_for('Index'))
 
 
#this is our update route where we are going to update a presence
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_presence = Presence.query.get(request.form.get('ID'))
 
        my_presence.chip_no = request.form['chip_no']
        my_presence.room_no = request.form['room_no']
        my_presence.date = request.form['date']
        my_presence.time_checkin = request.form['time_checkin']
        my_presence.time_checkout = request.form['time_checkout']
 
        db.session.commit()
        flash("Presence Updated Successfully")
 
        return redirect(url_for('Index'))
 
 
 
 
#This route is for deleting a presence
@app.route('/delete/<ID>/', methods = ['GET', 'POST'])
def delete(ID):
    my_presence = Presence.query.get(ID)
    db.session.delete(my_presence)
    db.session.commit()
    flash("Presence Deleted Successfully")
 
    return redirect(url_for('Index'))
 
 
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True, host ="0.0.0.0", port=5000)

