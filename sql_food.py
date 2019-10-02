# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 13:48:12 2019

@author: JakeC
"""

import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

sqlSelectQuery = """
SELECT DISTINCT facility_name FROM inspections, 
    violations WHERE violations.serial_number=inspections.serial_number"""
    
cursor.execute(sqlSelectQuery)

distinctiveBusinesses = sorted(cursor.fetchall())

for i in distinctiveBusinesses:
    print(i[0])
    
previousViolations_sql = "DROP TABLE IF EXISTS previous_violations;"
cursor.execute(previousViolations_sql)

previousViolations_sql = """
CREATE TABLE previous_violations (
    name varchar(100),
    address varchar(120),
    zipCode varchar(10),
    city varchar(60)
);"""

cursor.execute(previousViolations_sql)

sqlInsertQuery = """
INSERT INTO previous_violations SELECT facility_name, 
    facility_address, 
    facility_zip, 
    facility_city FROM inspections,
    violations WHERE violations.serial_number=inspections.serial_number GROUP BY facility_name"""
    
cursor.execute(sqlInsertQuery)

sqlSelectQuery = """
SELECT COUNT(violations.serial_number),
    facility_name FROM inspections, 
    violations WHERE violations.serial_number=inspections.serial_number GROUP BY facility_name ORDER BY COUNT(violations.serial_number) DESC"""
    
cursor.execute(sqlSelectQuery)

distinctiveBusinesses = cursor.fetchall()

for j in distinctiveBusinesses:
    print(j[1], j[0])
print(len(distinctiveBusinesses))

connection.commit()
connection.close()    