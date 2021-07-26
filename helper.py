import flask
from flask import request, jsonify
import psycopg2
import pandas as pd
import numpy as np
from flask_cors import CORS
import json
import _strptime
import datetime
from datetime import timedelta
import pandas.io.sql as sqlio
import os
import math
from ta import *

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required

from flask_bcrypt import Bcrypt 

import dateutil
import datetime

from dateutil.relativedelta import relativedelta, FR

from functools import reduce

app = flask.Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


with open('config.json','r') as f:
	config = json.load(f)

app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'BravisaTempleTreeEncryptedToken'


DBhost = config['DBLocal']['host']
DB = config['DBLocal']['DB']
DBuser = config['DBLocal']['DBuser']
DBPass = config['DBLocal']['DBPass']
DBPort = config['DBLocal']['DBPort']

today = datetime.date.today()
date1Yback = (today + datetime.timedelta(-365))
date30_back = (today + datetime.timedelta(-30))
date35_back = (date30_back + datetime.timedelta(-5))
date7back = (today+datetime.timedelta(-7))
day1forword = (date30_back + datetime.timedelta(1))

def db_connect():
    """ 
    User Input: Nothing

    Output: JSON format  (conn)

    Definition: Use to established database connection. 

    Description : It check the Operatinf system. If OS is Windows i.e. 'nt' then execute if part or else.
    """
    
    if os.name == 'nt':
        conn = psycopg2.connect(database=DB, user=DBuser, password=DBPass, host=DBhost, port=DBPort)
        app.config["DEBUG"] = True
        return conn
    else:
        conn = psycopg2.connect(database="BravisaDB", user="sid", password="kayasid2018", host="/cloudsql/bravisa-temple-tree:asia-south1:btt-db", port="5432")
        return conn

def db_connect_local():
	conn = psycopg2.connect(database="newdb", user="postgres", password="postgres")
	app.config["DEBUG"] = True
	return conn
   