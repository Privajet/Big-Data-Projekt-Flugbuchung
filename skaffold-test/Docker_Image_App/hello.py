#author: Aniket Mukherjee
from flask import Flask
import emoji
import pyjokes

app=Flask(__name__)

@app.route('/')
def hello():
  return pyjokes.get_joke()
  

@app.route('/fun')
def fun():
  return emoji.emojize('Python development with Skaffold is :thumbs_up:')