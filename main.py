#####################################################################################
# imports
#####################################################################################
import os
import glob
import pathlib
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


#####################################################################################
# input
#####################################################################################
path= "/data-confidential/"
separator= ";"
dbname= "postgres"
user= "postgres"
password= "postgres" 
host= "localhost"
port= "5432"


#####################################################################################
# main program
#####################################################################################
cwd = os.getcwd()
all_files = glob.glob(os.path.join(cwd+path, "*.csv"))

for f in all_files:
    print(f"reading {f}")
    df= pd.read_csv(f, sep= separator)
    
    time_column = [s for s in df.columns if "Leg Time" in s][0]
    df.insert(0, "epoch", pd.to_datetime(df[time_column],utc= True).values.astype(np.int64) // 10**6)
    print("successfully added time column to database")

    postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    print("connecting to "+postgres_url)

    try:
        table_name = f.split("/")[-1][0:-14]
        engine = create_engine(postgres_url)

        print(f"Uploading the data from {table_name} to postgres. This may take a while ...")
        df.to_sql(table_name, engine, if_exists='replace', index= False)
    except ValueError as vx:
        print(vx)
    except Exception as ex:  
        print(ex)
    else:
        print("Postgresql database filled successfully.")


