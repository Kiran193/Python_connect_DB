from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mongo_app"
app.config['MONGO_DBNAME'] = 'connection'
# app.config['SECRET_KEY'] = 'secret_key'

mongo = PyMongo(app)
db = mongo.db
# col = mongo.db["connection"]
print ("MongoDB Database:", mongo.db["connection"])

@app.route("/")
def connect_mongo():
    print ("Working")
    return db["connection"]

if __name__ == '__main__':
    app.run(debug=True)

