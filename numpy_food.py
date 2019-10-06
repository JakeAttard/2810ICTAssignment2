import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Check connection
con = sqlite3.connect("database.db")
print('Connection: OK')

#''' Question 1 '''

# Fetch data.
query1 = "select facility_zip,strftime('%m',activity_date) as month, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) desc limit 1) group by month"
df1 = pd.read_sql_query(query1, con)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(df1.month, df1.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {df1.facility_zip[0]}\n which has the highest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Month")
plt.show()
###############################################################

#''' Question 2 '''

# Fetch data.
query2 = "select facility_zip,strftime('%m',activity_date) as month, count(violations.serial_number) as num_of_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number and facility_zip=(select facility_zip from inspections, violations where violations.serial_number=inspections.serial_number group by facility_zip order by count(violations.serial_number) asc limit 1) group by month"
df2 = pd.read_sql_query(query2, con)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(df2.month, df2.num_of_viol_per_month)
plt.title(
    f"Violations per month for zip code {df2.facility_zip[0]}\n which has the lowest total violations")
plt.ylabel("Number of violations")
plt.xlabel("Month")
plt.show()

###############################################################
#''' Question 3 '''

# Fetch data.
query3 = "select strftime('%m',activity_date) as month, count(violations.serial_number)/count(distinct(facility_zip)) as avg_viol_per_month from inspections, violations where violations.serial_number=inspections.serial_number group by month"
df3 = pd.read_sql_query(query3, con)

# Plot the graph.
plt.figure(figsize=(8, 8))
plt.bar(df3.month, df3.avg_viol_per_month)
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
df41 = pd.read_sql_query(query41, con)
df42 = pd.read_sql_query(query42, con)

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
con.close()
print('Connection: Closed')