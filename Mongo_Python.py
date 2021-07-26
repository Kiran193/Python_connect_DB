import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

mydb = client['Employee'] 

information = mydb.employeeinformation
record = {
            'firstname':'Kiran',
            'lastname':'Thakur',
            'dept':'Data Science'
         }
information.insert_one(record)

record_list = [{
            'firstname':'Kiran1',
            'lastname':'Thakur1',
            'dept':'Data Science1'
         },
         {
            'firstname':'Kiran2',
            'lastname':'Thakur2',
            'dept':'Data Science2'
         },
         {
            'firstname':'Kiran3',
            'lastname':'Thakur3',
            'dept':'Data Science3'
         }]
information.insert_many(record_list)

#####  For fetch to get first record
one_record = information.find_one({})
print(one_record)

print("***********************")

####  For fetch multiple record
for record in information.find({}):
    print(record)

###  select * from employeeinformation where firstname='kiran'
for record in information.find({'firstname':'Kiran'}):
    print(record)

### Query documents using query operators($in, $lt, $gt)
for record in information.find({'dept':{'$in':['Data Science', 'Data Science1']}}):
    print(record)


### AND and Query operators
for record in information.find({'dept':'Data Science'}, {'firstname':'Kiran1'}):
    print(record)

### OR and Query operators
for record in information.find({'$or':[{'dept':'Data Science'}, {'firstname':'Kiran1'}]}):
    print(record)


# Create new collection in DataBase Employee

inventory = mydb.inventory
inventory.insert_many([
    {'items':"journal", 'qty':25, 'size': {'h':14, 'w':21, 'uom':"cm"}, 'status':"A"},
    {'items':"notebook", 'qty':50, 'size': {'h':8.5, 'w':11, 'uom':"in"}, 'status':"D"},
    {'items':"paper", 'qty':100, 'size': {'h':8.5, 'w':11, 'uom':"in"}, 'status':"D"},
    {'items':"planner", 'qty':75, 'size': {'h':22.85, 'w':30, 'uom':"cm"}, 'status':"A"},
    {'items':"postcard", 'qty':45, 'size': {'h':10, 'w':15.25, 'uom':"cm"}, 'status':"A"},

])

for record in inventory.find({'size':{'h':14, 'w':21, 'uom': "cm"}}):
    print(record)