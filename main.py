import flask
from flask import request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required
from flask_bcrypt import Bcrypt 
from flask_cors import CORS

import _strptime
import datetime
from datetime import timedelta
import dateutil
from dateutil.relativedelta import relativedelta, FR

import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
import numpy as np
import json
import os
import math
from ta import *
from werkzeug.security import safe_str_cmp
from functools import reduce

app = flask.Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# cloud_sql_proxy -instances=bravisa-temple-tree:asia-south1:btt-db=tcp:5444

import flask_login

import json
import time


with open('config.json','r') as f:
	config = json.load(f)

app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'BravisaTempleTreeEncryptedToken'


DBhost = config['DBLocal']['host']
DB = config['DBLocal']['DB']
DBuser = config['DBLocal']['DBuser']
DBPass = config['DBLocal']['DBPass']
DBPort = config['DBLocal']['DBPort']

def db_connect():
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


@app.route('/register', methods=['POST'])
def register():

	conn = helper.db_connect()
	cur = conn.cursor()
	
	username = request.json['username']
	password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

	cur.execute("INSERT INTO \"public\".users (username, password) VALUES ('" +
		str(username) + "','" +
		str(password) + "')")

	conn.commit()
	result = {
		'username': username,
		'password': password
	}
	conn.close()

	return jsonify({'result': result})

@app.route('/login', methods=['POST'])
def login():

	conn = helper.db_connect()
	cur = conn.cursor()

	username = request.json['username']
	password = request.json['password']
	result = ""
	
	cur.execute("SELECT * FROM \"public\".users where username = '" + str(username) + "'")
	details = cur.fetchone()

	if bcrypt.check_password_hash(details[1], password):
		access_token = create_access_token(identity = {'username': details[0]}, expires_delta=timedelta(seconds=28800))
		result = jsonify({"token":access_token})
	else:
		result = jsonify({"error": "Invalid credentials"})
	
	conn.close()
	return result 


@app.route('/API_NAME', methods=['GET'])
@jwt_required
def function_name_api():
    return Suite().functionName()


@app.route('/API_NAME', methods=['GET', 'PUT'])
@jwt_required
def function_name_api():
    return className().functionName()



if __name__=="__main__":
	app.debug = True
	app.run(host='127.0.0.1', port=8081)
