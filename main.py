
# imports
import psycopg2

# connect to server
conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432")

# issue commands using cursor
cur = conn.cursor()
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