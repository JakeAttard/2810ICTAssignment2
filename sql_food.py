# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 13:48:12 2019

@author: JakeC
"""
# Importing sqlite3
import sqlite3

# Connecting to the sqlite3 database called database.db
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# SQL Command to get the data from the database
sqlSelectQuery = """
SELECT DISTINCT facility_name FROM inspections, 
    violations WHERE violations.serial_number=inspections.serial_number"""
    
cursor.execute(sqlSelectQuery)

# Sorting all the data fetched from the database into a variable called distinctiveBusinesses.
distinctiveBusinesses = sorted(cursor.fetchall())

# Looping through the data and printing it to the console.
for i in distinctiveBusinesses:
    print(i[0])

# SQL Command dropping the table called previous_violations if it currently exists.
previousViolations_sql = "DROP TABLE IF EXISTS previous_violations;"
cursor.execute(previousViolations_sql)

# SQL Command for creating a new table within the database
previousViolations_sql = """
CREATE TABLE previous_violations (
    name varchar(100),
    address varchar(120),
    zipCode varchar(10),
    city varchar(60)
);"""

cursor.execute(previousViolations_sql)

# SQL Command for inserting the data into the database table called previous_violations
sqlInsertQuery = """
INSERT INTO previous_violations SELECT facility_name, 
    facility_address, 
    facility_zip, 
    facility_city FROM inspections,
    violations WHERE violations.serial_number=inspections.serial_number GROUP BY facility_name"""
    
cursor.execute(sqlInsertQuery)

# SQL Command for getting the count of all violations for each businesses
sqlSelectQuery = """
SELECT COUNT(violations.serial_number),
    facility_name FROM inspections, 
    violations WHERE violations.serial_number=inspections.serial_number GROUP BY facility_name ORDER BY COUNT(violations.serial_number) DESC"""
    
cursor.execute(sqlSelectQuery)

# Fetching all the data from the database in a variable called distinctiveBusinesses
distinctiveBusinesses = cursor.fetchall()

# Looping through the data and printing it to the console, along with the count length of all violations.
for j in distinctiveBusinesses:
    print(j[1], j[0])
print(len(distinctiveBusinesses))

# Saves and closes the connection
connection.commit()
connection.close()    