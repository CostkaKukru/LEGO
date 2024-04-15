import mysql.connector as mysql_import
import pandas as pd
import os

path = "brickset-sets" # setting a path to the files
folder = os.fsencode(path)  
filenames = []

for file in os.listdir(folder): 
    filename = os.fsdecode(file)
    if filename.endswith( ('.csv',) ): # choosing a file type
        filenames.append(filename)
filenames.sort() # sorting filenames list
parent_dir = "/Users/Ola/Downloads/LEGO Sets Database/brickset-sets/"

# connect to MySQL database
conn = mysql_import.connect(host='localhost', user='root', password='1234', database='lego')
cursor = conn.cursor()

# iterate through CSV files
csv_files = [parent_dir + s for s in filenames]  # list of CSV file paths

# extract data from two particular columns in .csv file
for file in csv_files:
    df = pd.read_csv(file)
    price_data = df[['Number', 'RRP (USD)']] 
          
    # iterate through the price data and update corresponding rows in the 'sets' table
    for index, row in price_data.iterrows():
        set_num = row['Number']
        price_usd = row['RRP (USD)']
        
        # construct the SQL query to update 'price_USD' column in 'sets' table
        sql_query = "UPDATE sets SET price_USD = %s WHERE set_num = %s"
        
        # execute the SQL query with price data and set_num as parameters
        cursor.execute(sql_query, (price_usd, set_num))
        
# Commit changes and close connection
conn.commit()
conn.close()
