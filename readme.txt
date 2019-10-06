This data analysis and visualisation project contains five tasks which use sqlite3 for the database, python, excel, numpy, matplotlib and documentation. 

Instructions
1. Please make sure that you have installed in your enviroment Visual Studio Code, Python 3 with the packages pandas, matplotlib and sqlite3. If you don't, please use 'pip' to install them on your machine and then run the file 'createdb_food.py'.
2. In order to a connection to be established, the database ('database.db') and the script should be in the same folder.
3. The queries will take significant time to fetch and edit the data. Be patient!
4. Each plot that is displayed on your screen, close it or save it, in order to begin the next query to fetch data . If you don't, the system will wait endlessly for an action.
5. All the calculations are being done from the SQL engine in the background, so the code will be simpler and cleaner.

Task 1 (createdb_food.py) required to create a sqlite3 database importing all the food violations data from the excel files inspections.xlsx and violations.xlsx.

Task 2 (sql_food.py) required to list all the distinctive businesses that have had at least 1 violation ordered alphabetically to the console and saving it in a database table called previous_violations.

Task 3 (excel_food.py) required to create a new excel worksheet called ViolationTypes.xlsx querying the database to calculate the number of each type of violations based on the violation code.

Task 4 (numpy_food.py) required to create graphs based on the:
    -The number of violations per month for the postcode with the highest total violations.
    -The number of violations per month for the postcode with the lowest total violations.
    -The average number of violations per month for all of California.
    -The average number of violations per month for all McDonalds compared with the averga number of violations for all burger kings.

Task 5 (s5138647_JakeAttard_ReportDocument.docx) is the documentation and summary of the report.