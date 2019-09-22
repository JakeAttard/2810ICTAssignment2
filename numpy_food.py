# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 15:34:03 2019

@author: JakeC
"""

import numpy
import sqlite3
import matplotlib.pyplot as plt

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

violationsTotalPostcode = dict()
violationsTotalMonth = dict()
violationsMonthAverage = list()
violationsPostcode = list()
violationsDifferentPostcodes = list()
lastPostcode = 0
minimumValue = 0
difference = 0

sqlSelectQuery = """
SELECT COUNT(violations.serial_number),
    facility_zip,
    strftime('%m-%Y, activity_date) FROM violations,
    inspections WHERE violations.serial_number=inspections.serial_number GROUP BY facility_zip,
    strftime('%m', activity_date) ORDER BY facility_zip,
    strftime('%Y-%m', activity_date) DESC"""
    
cursor.execute(sqlSelectQuery)
data = cursor.fetchall()

for i in data:
    violationsTotalPostcode[i[1]] = violationsTotalPostcode.get(i[1], 0) + i[0]
    violationsTotalMonth[i[2]] = violationsTotalMonth.get(i[2], [])
    violationsTotalMonth[i[2]].append(i[0])
    if i[1] == lastPostcode:
        if difference < (abs(i[0] - minimumValue)):
            difference = (abs(i[0] - minimumValue))
            postcodeDifference = i[1]
        elif minimumValue > i[0]:
            minimumValue = i[0]
    lastPostcode = i[1]
    
for key, value in violationsTotalMonth.items():
    violationsMonthAverage.append([key, sum(value) / len(value)])

largestAmountViolations = max(violationsTotalPostcode, key = violationsTotalPostcode.get)

for j in data:
    if j[1] == largestAmountViolations:
        violationsPostcode.append((j[2], j[0]))
    if postcodeDifference == j[1]:
        violationsDifferentPostcodes.append((j[2], j[0]))
        
for date in violationsMonthAverage:
    date[0] = date[0][3:] + '-' + date[0][:2]
violationsMonthAverage = sorted(violationsMonthAverage)

violationsPostcode.reverse()
violationsDifferentPostcodes.reverse()

