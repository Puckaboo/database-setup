
# imports
import psycopg2

# connect to server
conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432")