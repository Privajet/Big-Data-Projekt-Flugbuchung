#author: Aniket Mukherjee
from flask import Flask, render_template
import emoji
import pyjokes
import socket
# from flask_caching import Cache
# import psycopg2
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import ForeignKeyConstraint, ForeignKey
# from sqlalchemy.orm import relationship, backref
 
#import playsound



app=Flask(__name__)
@app.route('/')
def hello():


    return render_template('index.html')

@app.route('/test')
def test():
    config = {
        "DEBUG": True,          # some Flask specific configs
        "CACHE_TYPE": "MemcachedCache",  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_MEMCACHED_SERVERS":"memcached",
    }

    app.config.from_mapping(config)
    cache = Cache(app)
    return emoji.emojize('Python development with Skaffold is :thumbs_up:')
  
