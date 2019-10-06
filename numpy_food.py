import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connecting to the database
connection = sqlite3.connect("database.db")

# Testing to see if the connection is successful with the database
print('Connection successful')

#Task 4 Part 1
#The number of violations per month for the postcode with the highest total violations

# Fetching data from the database
query1 = "select facility_zip,strftime('%m',activity_date) as month, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) desc limit 1) group by month"
figure1 = pd.read_sql_query(query1, connection)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(figure1.month, figure1.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {figure1.facility_zip[0]}\n which has the highest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Months")
plt.show()

# Task 4 Part 2
# The number of violations per month for the postcode with the lowest total violations

# Fetching data from the database
query2 = "select facility_zip,strftime('%m',activity_date) as month, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) asc limit 1) group by month"
figure2 = pd.read_sql_query(query2, connection)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(figure2.month, figure2.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {figure2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Months")
plt.show()

# Task 4 Part 3
# The average number of violations per month for all McDonalds compared with the average number of violations for all burger kings.

# Fetching data from the database
query3 = "select strftime('%m',activity_date) as month, count(violations.serial_number)/count(distinct(facility_zip)) as avg_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number group by month"
figure3 = pd.read_sql_query(query3, connection)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(figure3.month, figure3.avg_viol_per_month)
plt.title("Average number of violations per month\n for all of California")
plt.ylabel("Average")
plt.xlabel("Month")
plt.show()

###############################################################

#''' Plot the three first graphs together '''

# Plot the graph.
plt.figure(figsize=(13, 13))
plt.subplot(2, 2, 1)
plt.bar(df1.month, df1.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {df1.facility_zip[0]}\n which has the highest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Month")

plt.subplot(2, 2, 2)

plt.bar(df2.month, df2.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {df2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Month")

plt.subplot(2, 2, 3)
plt.bar(df3.month, df3.avg_viol_per_month)
plt.title("Average number of violations per month\n for all of California")
plt.ylabel("Average")
plt.xlabel("Month")

plt.show()


#''' Question 4 '''

# Average number of violations per month for all Burger Kings
query41 = "select strftime('%m',activity_date) as month, count(violations.serial_number)/(select count(distinct(facility_name)) from inspections where facility_name LIKE '%BURGER KING%') as avg_num_viol_pm_BK from violations, inspections where violations.serial_number=inspections.serial_number and facility_name LIKE '%BURGER KING%' group by month"

# Average number of violations per month for all Macdonalds
query42 = "select strftime('%m',activity_date) as month, count(violations.serial_number)/(select count(distinct(facility_name)) from inspections where facility_name LIKE '%MCDONALDS%') as avg_num_viol_pm_MC from violations, inspections where violations.serial_number=inspections.serial_number and facility_name LIKE '%MCDONALDS%'group by month"

# Fetch data.
df41 = pd.read_sql_query(query41, connection)
df42 = pd.read_sql_query(query42, connection)

# Plot the graph.
plt.figure(figsize=(15, 15))
plt.subplot(2, 1, 1)
plt.bar(df41.month, df41.avg_num_viol_pm_BK)
plt.title('Average number of violations per month\n for Burger Kings and MCDonalds')
plt.ylabel('Average for\n Burger King')

plt.subplot(2, 1, 2)
plt.bar(df42.month, df42.avg_num_viol_pm_MC, color='green')
plt.xlabel('Month')
plt.ylabel('Average for\n McDonalds')

plt.show()
###############################################################
connection.close()
print('Connection: Closed')