import psycopg2
import flask
from flask import request, jsonify
import os
import json
from flask_bcrypt import Bcrypt 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required
from datetime import timedelta

app = flask.Flask(__name__)
bcrypt = Bcrypt(app)

with open('config.json','r') as f:
	config = json.load(f)

app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'SECRETKEY'


DBhost = config['DBLocal']['host']
DB = config['DBLocal']['DB']
DBuser = config['DBLocal']['DBuser']
DBPass = config['DBLocal']['DBPass']
DBPort = config['DBLocal']['DBPort']


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
        conn = psycopg2.connect(database="DBNAME", user="USERNAME", password="PASSWORD", host="HOSTNAMEIP_or_NAME", port="PORT")
        return conn

def db_connect_local():

    conn = psycopg2.connect(database="DBNAME", user="USERNAME", password="PASSWORD")
    app.config["DEBUG"] = True
    print(conn)
    return conn



# db_connect_local()  

def register():

	conn = db_connect_local()
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

# @app.route('/login', methods=['POST'])
def login():

	conn = db_connect_local()
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
