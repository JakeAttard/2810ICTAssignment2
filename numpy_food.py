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
query1 = "select facility_zip,strftime('%Y-%m',activity_date) as date, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) desc limit 1) group by date"
figure1 = pd.read_sql_query(query1, connection)

# Plot the graph.
plt.figure(figsize=(15, 10))
plt.plot(figure1.date, figure1.num_of_viol_per_month)
plt.title(
    f"Violations per month for postcode {figure1.facility_zip[0]}\n which has the highest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.show()

# Task 4 Part 2
# The number of violations per month for the postcode with the lowest total violations

# Fetching data from the database
query2 = "select facility_zip,strftime('%Y-%m',activity_date) as date, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) asc limit 1) group by date"
figure2 = pd.read_sql_query(query2, connection)

# Plot the graph.
plt.figure(figsize=(15, 10))
plt.bar(figure2.date, figure2.num_of_viol_per_month)
plt.title(
    f"Violations per month for postcode {figure2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.show()

# Plot the graph as a scatter.
plt.figure(figsize=(15, 10))
plt.scatter(figure2.date, figure2.num_of_viol_per_month)
plt.title(
    f"Violations per month for postcode {figure2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.show()

# Task 4 Part 3
# The average number of violations per month for all McDonalds compared with the average number of violations for all burger kings.

# Fetching data from the database
query3 = "select strftime('%Y-%m',activity_date) as date, count(violations.serial_number)/count(distinct(facility_zip)) as avg_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number group by date"
figure3 = pd.read_sql_query(query3, connection)

# Plot the graph.
plt.figure(figsize=(15, 10))
plt.plot(figure3.date, figure3.avg_viol_per_month)
plt.title("Average number of violations per month\n for all of California")
plt.ylabel("Average")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.show()

# Task 4 Part 1, 2, 3 combined together in one graph.

# Figure 1

# Plot the graph.
plt.figure(figsize=(20, 20))
plt.subplot(2, 2, 1)
plt.plot(figure1.date, figure1.num_of_viol_per_month)
plt.title(
    f"Violations per month for postcode {figure1.facility_zip[0]}\n which has the highest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Date")
plt.xticks(rotation=45)

# Figure 2 

# Plot the graph.
plt.subplot(2, 2, 2)
plt.scatter(figure2.date, figure2.num_of_viol_per_month)
plt.title(
    f"Violations per month for postcode {figure2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Date")


# Figure 3

# Plot the graph.
plt.subplot(2, 2, 3)
plt.plot(figure3.date, figure3.avg_viol_per_month)
plt.title("Average number of violations per month\n for all of California")
plt.ylabel("Average")
plt.xlabel("Date")
plt.xticks(rotation=45)
plt.show()


# Task 4 Part 4

# Average number of violations per month for all Burger Kings
burgerKingQuery = "select strftime('%Y-%m',activity_date) as date, count(violations.serial_number)/(select count(distinct(facility_name)) from inspections where facility_name LIKE '%BURGER KING%') as avg_num_viol_pm_BK from violations, inspections where violations.serial_number=inspections.serial_number and facility_name LIKE '%BURGER KING%' group by date"

# Average number of violations per month for all McDonalds
mcdonaldsQuery = "select strftime('%Y-%m',activity_date) as date, count(violations.serial_number)/(select count(distinct(facility_name)) from inspections where facility_name LIKE '%MCDONALDS%') as avg_num_viol_pm_MC from violations, inspections where violations.serial_number=inspections.serial_number and facility_name LIKE '%MCDONALDS%'group by date"

# Fetch data.
burgerKingFigure = pd.read_sql_query(burgerKingQuery, connection)
mcdonaldsFigure = pd.read_sql_query(mcdonaldsQuery, connection)

# Plot the graph.
plt.figure(figsize=(15, 10))
plt.subplot(2, 1, 1)
plt.plot(burgerKingFigure.date, burgerKingFigure.avg_num_viol_pm_BK)
plt.title('Average number of violations per month\n for Burger Kings and McDonalds')
plt.ylabel('Average for\n Burger King')
plt.xticks(rotation=45)

plt.subplot(2, 1, 2)
plt.plot(mcdonaldsFigure.date, mcdonaldsFigure.avg_num_viol_pm_MC, color='green')
plt.xlabel('Date')
plt.ylabel('Average for\n McDonalds')
plt.xticks(rotation=45)
plt.show()

# Task 4 Part 4 in one graph
plt.figure(figsize=(15, 10))
fig, ax = plt.subplots()
ax.plot(burgerKingFigure.date, burgerKingFigure.avg_num_viol_pm_BK, label="Burger King")
ax.plot(mcdonaldsFigure.date, mcdonaldsFigure.avg_num_viol_pm_MC, label="McDonalds")
ax.legend()
plt.xticks(rotation=45)
plt.title('Average number of violations per month\n for Burger Kings and McDonalds')
plt.show()

# Closing the database connection
connection.close()

# Prints to let the user know that the connection has closed successfully.
print('Connection closed successfully')