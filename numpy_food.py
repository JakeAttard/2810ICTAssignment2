# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 15:34:03 2019

@author: JakeC
"""

import numpy
import sqlite3
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter

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
    strftime('%m-%Y', activity_date) FROM violations,
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

# ViolationsPostcode
valueX = [x[0] for x in violationsPostcode]
valueY = [y[1] for y in violationsPostcode]
plt.xticks(range(len(valueY)), valueX)
plt.plot(valueY)
plt.title(('Violations per month for zip code {} which has the highest total violations').format(largestAmountViolations))
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()

valueX = [x[0] for x in violationsDifferentPostcodes]
valueY = [y[1] for y in violationsDifferentPostcodes]
plt.xticks(range(len(valueY)), valueX)
plt.plot(valueY)
plt.title(('Violations per month for zip code {} which has the greatest variance').format(postcodeDifference))
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()

valueX =[x[0].replace('20','') for x in violationsMonthAverage]
valueY = [y[1] for y in violationsMonthAverage]
plt.xticks(range(len(valueY)), valueX)
plt.plot(valueY)
plt.title('Total violations per month for all zip codes')
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()

#### Average number of violations per month for all McDonalds compared with average for all Burger Kings.

query = """SELECT COUNT(violations.serial_number), strftime('%Y-%m', activity_date), facility_name
FROM violations, inspections
WHERE violations.serial_number=inspections.serial_number AND (facility_name LIKE '%BURGER KING%' OR facility_name LIKE '%MCDONALDS%')
GROUP BY facility_name, strftime('%m',activity_date)
ORDER BY  facility_name , strftime('%Y-%m', activity_date) DESC
"""
cursor.execute(query)
result = cursor.fetchall()

restraunt = dict()
x = list()
y = list()
for item in result:
    restraunt[item[1]] = restraunt.get(item[1], 0) + item[0]
for key, value in restraunt.items():
    x.append(key)
    y.append(value)
plt.xticks(range(len(valueY)), valueX)
plt.plot(valueX)
plt.title('Total violations per month for all burger kings and mcdonalds')
plt.xlabel('Date')
plt.ylabel('Number of violations')
plt.show()
