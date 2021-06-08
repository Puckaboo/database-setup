#####################################################################################
# imports
#####################################################################################
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


#####################################################################################
# input
#####################################################################################
data_path= "./data/data_small.csv"
time_column= "S7 Leg SBFore Data Data Leg Time"
table_name = "challenger"
dbname= "postgres"
user= "postgres"
password= "postgres" 
host= "localhost"
port= "5432"


#####################################################################################
# main program
#####################################################################################
df= pd.read_csv(data_path)

df.insert(0, "epoch", pd.to_datetime(df[time_column],utc= True).values.astype(np.int64) // 10**6)
print("successfully added time column to database")

postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print("connecting to "+postgres_url)

try:
    print("Uploading the data to postgres. This may take a while ...")
    engine = create_engine(postgres_url)
    df.to_sql(table_name, engine, if_exists='replace', index= False)
except ValueError as vx:
    print(vx)
except Exception as ex:  
    print(ex)
else:
    print("Postgresql database filled successfully.")


