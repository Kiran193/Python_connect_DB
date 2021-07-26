from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from pymodm.connection import connect

# Connect to MongoDB and call the connection "my-app".
connect("mongodb://127.0.0.1:27017/mongo_app", alias="mongo_app")


class Connection(MongoModel):
    established = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
    
    def establish(self):
        Connection("established").save()

        for c in Connection.objects.all():
            if c.established == "established":
                return True

if __name__ == "__main__":
    conn = Connection()
    conn.establish()
