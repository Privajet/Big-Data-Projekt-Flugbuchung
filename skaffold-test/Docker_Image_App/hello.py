#author: Aniket Mukherjee
from flask import Flask
import emoji
import pyjokes

app=Flask(__name__)

@app.route('/')
def hello():
    html = "<h3>Hello World from {hostname}!</h3>"
    return html.format(hostname=socket.gethostname())
  

@app.route('/fun')
def fun():
  return emoji.emojize('Python development with Skaffold is :thumbs_up:')
  
@app.route('/')
def hello():
    html = "<h3>Hello World from {hostname}!</h3>"
    return html.format(hostname=socket.gethostname())