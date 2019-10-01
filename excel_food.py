# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 22:38:21 2019

@author: JakeC
"""
import openpyxl as xl
from openpyxl import Workbook
import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

wb = Workbook()
wbs1 = wb.active

wbs1.title = "Violation Types"
wbs1["A1"] = "Code"
wbs1["B1"] = "Description"
wbs1["C1"] = "Count"

print(wb.sheetnames)

sqlSelectQuery = """
SELECT violation_code,
    violation_description,
    COUNT(violation_code) FROM violations GROUP BY violation_code ORDER BY violation_code"""

cursor.execute(sqlSelectQuery)

violationTypes = cursor.fetchall()

for i in violationTypes:
    wbs1.append(i)

#for a, b in zip(wbs1.iter_rows(min_row = 2, min_col = 1, max_col = 3), violationTypes):
#    for i in range(3):
#        a[i].value = b[i]
        
counter = 0
for row in wbs1.iter_rows(min_row = 2):
    count = row[2].value
    counter += count

lastRow = wbs1.max_row

wbs1["B118"] = "Total Sum"

wbs1['C' + str(lastRow + 1) ] = int(counter)
wb.save("ViolationTypes.xlsx")