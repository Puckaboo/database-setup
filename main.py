
#####################################################################################
# imports
#####################################################################################
import psycopg2

#####################################################################################
# input
#####################################################################################
table_name = 'users'
server_credentials= {
    'dbname': "postgres", 
    'user': "postgres", 
    'password':"postgres", 
    'host': "localhost", 
    'port': "5432"
}

#####################################################################################
# functions
#####################################################################################
def exists_table(table):
    pass

#####################################################################################
# connect to postgresql server
#####################################################################################
conn = psycopg2.connect(**server_credentials)

#####################################################################################
# create a data table
#####################################################################################
# issue commands using cursor
cur = conn.cursor()

# check if the table exists
cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table_name,))
table_exists = cur.fetchone()[0]

# create the table and insert data
if (not table_exists):
    cur.execute(
    """
        CREATE TABLE users(
        id integer PRIMARY KEY,
        email text,
        name text,
        address text
    )
    """
    )
    conn.commit()

# insert the data from the .csv
with open('./data/users.csv', 'r') as f:
    next(f) # Skip the header row.
    cur.copy_from(f, 'users', sep=',')
conn.commit()