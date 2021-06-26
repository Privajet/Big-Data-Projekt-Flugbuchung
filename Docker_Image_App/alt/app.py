
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
 

 
app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration With Mysql
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgres',url='localhost',db='ccmgmtdb')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)


 
 
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
        





#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_presence = Presence.query.all()
 
    return render_template("index.html", presence = all_presence)
 
 
 

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
 
 
#this is our update route where we are going to update our employee
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
 
 
 
 
#This route is for deleting our employee
@app.route('/delete/<ID>/', methods = ['GET', 'POST'])
def delete(ID):
    my_presence = Presence.query.get(ID)
    db.session.delete(my_presence)
    db.session.commit()
    flash("Presence Deleted Successfully")
 
    return redirect(url_for('Index'))
 
 
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)