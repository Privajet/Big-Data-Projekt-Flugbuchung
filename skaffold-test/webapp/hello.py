#author: Aniket Mukherjee
from flask import Flask, render_template
import emoji
import pyjokes
import socket
#import playsound





app=Flask(__name__)
@app.route('/')
def hello():
   
    
    return render_template('index.html')
  

@app.route('/fun')
def fun():
  return emoji.emojize('Python development with Skaffold is :thumbs_up:')
  
