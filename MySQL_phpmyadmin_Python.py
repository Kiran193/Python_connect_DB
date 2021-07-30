# pip install pymysql

import pymysql
from pymysql.cursors import Cursor

def db_connect():

    #database connection
    connection = pymysql.connect(user='USERNAME', 
                                password='PASSWORD',
                                host='hostIPorName',
                                database='DBNAME' )
    # cnx = mysql.connector.connect(user='root', password='root@123',
    #                                 host='hostIPorName',
    #                                 database='DBNAME')
    cursor = connection.cursor()

    return cursor, connection

def create_table():
    cursor, connection = db_connect()
    # Query for creating table
    ArtistTableSql = """CREATE TABLE Artists(
    ID INT(20) PRIMARY KEY AUTO_INCREMENT,
    NAME  CHAR(20) NOT NULL,
    TRACK CHAR(10))"""

    cursor.execute(ArtistTableSql)
    connection.close()


def select_data():
    cursor, connection = db_connect()
    # queries for retrievint all rows
    retrive = "Select * from tbl_tablename;"

    #executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


    #commiting the connection then closing it.
    connection.commit()


    connection.close()


# # some other statements  with the help of cursor
# connection.close()

select_data()
