from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
import mysql.connector
from mysql.connector import cursor

# from __future__ import print_function
from datetime import date, datetime, timedelta
##### MySQL Connection
def mysql_cursor():
    # cnx = mysql.connector.connect(user='root', password='mysql',
    #                             host='127.0.0.1',
    #                             database='connection_test')

    cnx = mysql.connector.connect(user='pmsdb', 
                                password='pms@1234',
                                host='192.168.0.236',
                                database='pms')
    print(cnx)
    cursor = cnx.cursor()

    return cnx, cursor



##### Create Table

DB_NAME = 'connection_test'

TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

TABLES['departments'] = (
    "CREATE TABLE `departments` ("
    "  `dept_no` char(4) NOT NULL,"
    "  `dept_name` varchar(40) NOT NULL,"
    "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
    ") ENGINE=InnoDB")

TABLES['salaries'] = (
    "CREATE TABLE `salaries` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `salary` int(11) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_emp'] = (
    "CREATE TABLE `dept_emp` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `dept_no` char(4) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['dept_manager'] = (
    "  CREATE TABLE `dept_manager` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `dept_no` char(4) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`,`dept_no`),"
    "  KEY `emp_no` (`emp_no`),"
    "  KEY `dept_no` (`dept_no`),"
    "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
    "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
    "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


# cnx = mysql.connector.connect(user='root')

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_select_DB():
    try:
        print("Select DB")
        cnx, cursor = mysql_cursor()
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

def create_table(TABLES):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cnx, cursor = mysql_cursor()
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
    cnx.close()

def insert_data():

    cnx, cursor = mysql_cursor()

    tomorrow = datetime.now().date() + timedelta(days=1)

    add_employee = ("INSERT INTO employees "
                "(first_name, last_name, hire_date, gender, birth_date) "
                "VALUES (%s, %s, %s, %s, %s)")

    data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

    # Insert new employee
    cursor.execute(add_employee, data_employee)
    emp_no = cursor.lastrowid

    # Insert salary information
    add_salary = ("INSERT INTO salaries "
                "(emp_no, salary, from_date, to_date) "
                "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")
                
    data_salary = {
            'emp_no': emp_no,
            'salary': 50000,
            'from_date': tomorrow,
            'to_date': date(9999, 1, 1),
            }
    cursor.execute(add_salary, data_salary)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def use_query():
    # import datetime
    # import mysql.connector

    # cnx = mysql.connector.connect(user='scott', database='employees')
    # cursor = cnx.cursor()

    cnx, cursor = mysql_cursor()

    query = ("SELECT first_name, last_name, hire_date FROM employees "
            "WHERE hire_date BETWEEN %s AND %s")

    hire_start = datetime(1999, 1, 1)
    hire_end = datetime(2021, 12, 31)

    data = cursor.execute(query, (hire_start, hire_end))

    if data == None:
        print("No one hired during {} to {}", hire_start, hire_end)
    else:
        for (first_name, last_name, hire_date) in cursor:
            print("{}, {} was hired on {:%d %b %Y}".format(
                last_name, first_name, hire_date))

        cursor.close()
    cnx.close()

def use_query_pms():
    # import datetime
    # import mysql.connector

    # cnx = mysql.connector.connect(user='scott', database='employees')
    # cursor = cnx.cursor()

    cnx, cursor = mysql_cursor()

    print(cursor)

    query = ("SELECT * FROM activity_tbl;")

    # hire_start = datetime(1999, 1, 1)
    # hire_end = datetime(2021, 12, 31)

    data = cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    if rows == None:
        print("No Data ")
    else:
        print("Data Found")

    cursor.close()
    cnx.close()

# create_select_DB()
# create_table(TABLES)

# insert_data()
# use_query()
use_query_pms()

# cursor object properties :
# column_names, description, lastrowid, rowcount, statement

