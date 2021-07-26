from pymodm.connection import connect
from connection import Connection
# Connect to MongoDB and call the connection "my-app".

def dbconnect():
    connect("mongodb://127.0.0.1:27017/mongo_app", alias="mongo_app") 
    Connection("established").save()
    return Connection.established


if __name__ == "__main__":
    result = dbconnect()
    print("Result: ", result)
# for conn in connect.objects.all():
#     print("Result: ", conn)

