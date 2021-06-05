#####################################################################################
# imports
#####################################################################################
import pandas as pd
from sqlalchemy import create_engine


#####################################################################################
# input
#####################################################################################
data_path = "./data/data_large.csv"
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

postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
print("connecting to "+postgres_url)

try:
    print("Uploading the data to postgres. This may take a while ...")
    engine = create_engine(postgres_url)
    df.to_sql(table_name, engine, if_exists='replace')
except ValueError as vx:
    print(vx)
except Exception as ex:  
    print(ex)
else:
    print("Postgresql database filled successfully.")


