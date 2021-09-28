#####################################################################################
# imports
#####################################################################################
import os
import glob
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2


#####################################################################################
# input
#####################################################################################
print('Type folder name:')
path= '/'+input()
print('Time column name:')
time_column_name = input()
separator= ";"
dbname= "postgres"
user= "postgres"
password= "postgres" 
host= "localhost"
port= "5432"


#####################################################################################
# helper functions
#####################################################################################
def psycopg2_add_to_table(conn, df):
    # https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join([f'"{x}"' for x in list(df.columns)])
    query  = "INSERT INTO %s(%s) VALUES %%s" % (f'"{table_name}"', cols)
    cursor = conn.cursor()
    try:
        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()

#####################################################################################
# main program
#####################################################################################
cwd = os.getcwd()
all_files = glob.glob(os.path.join(cwd+path, "*.csv"))

table_names = []

postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print("connecting to "+postgres_url)
engine = create_engine(postgres_url)   

for f in all_files:
    print(f"reading {f}")
    df= pd.read_csv(f, sep= separator)
    
    time_column = [s for s in df.columns if time_column_name in s][0]
    df.insert(0, "epoch", pd.to_datetime(df[time_column],utc= True).values.astype(np.int64) // 10**6)
    print("successfully added time column to database")

    try:
        table_name = f.split("/")[-1][0:-14]
        if table_name not in table_names:
            print(f"Uploading the data from {table_name} to postgres. This may take a while ...")
            df.to_sql(table_name, engine, if_exists='replace', index= False)
            table_names += [table_name]
        else:
            print(f'{table_name} is already present in database. Existing data is appended.')
            conn = psycopg2.connect(f"""dbname={dbname} 
                                        user={user}
                                        password={password}
                                        host={host}
                                        port={port}""")
            psycopg2_add_to_table(conn, df)        
    except ValueError as vx:
        print(vx)
    except Exception as ex:  
        print(ex)
    else:
        print("Postgresql database filled successfully.")


