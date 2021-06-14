#####################################################################################
# imports
#####################################################################################
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from tqdm import tqdm


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
# function definitions
#####################################################################################

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def insert_with_progress(df):
    chunksize = int(len(df) / 10)
    with tqdm(total=len(df)) as pbar:
        for i, cdf in enumerate(chunker(df, chunksize)):
            replace = "replace" if i == 0 else "append"
            cdf.to_sql(table_name, engine , if_exists="append", index=False) 
            pbar.update(chunksize)
            tqdm._instances.clear()

#####################################################################################
# main program
#####################################################################################
df= pd.read_csv(data_path)

postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print("connecting to "+postgres_url)

df.insert(0, "epoch", pd.to_datetime(df[time_column],utc= True).values.astype(np.int64) // 10**6)
print("successfully added time column to database")

df_copy = df.copy()

try:
    print("Uploading the data to postgres. This may take a while ...")
    engine = create_engine(postgres_url)
    insert_with_progress(df_copy)
except ValueError as vx:
    print(vx)
except Exception as ex:  
    print(ex)
else:
    print("Postgresql database filled successfully.")


