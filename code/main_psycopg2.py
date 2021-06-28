
#####################################################################################
# imports
#####################################################################################
import psycopg2
from psycopg2 import Error

#####################################################################################
# input
#####################################################################################
data_path = "./data/users.csv"
table_name = "users"
server_credentials= {
    "dbname": "postgres", 
    "user": "postgres", 
    "password":"postgres", 
    "host": "localhost", 
    "port": "5432"
}

#####################################################################################
# main program
#####################################################################################
try:
    # connect to the server
    connection = psycopg2.connect(**server_credentials)
    cursor = connection.cursor()

    # create the table
    cursor.execute(
        """
            CREATE TABLE users(
            id integer PRIMARY KEY,
            email text,
            name text,
            address text
        )
        """
    )
    connection.commit()
    print(f"successfully created a table named {table_name}")

    # add the data
    with open(data_path, 'r') as f:
        next(f) # Skip the header row.
        cursor.copy_from(f, 'users', sep=',')
    connection.commit()
    print("successfully added the data from the .csv")

except (Exception, Error) as error:
    print("The following error occured: ", error)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")