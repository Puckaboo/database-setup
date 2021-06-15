# database-setup
This code imports data from .csv files, stores it in a pandas dataframe to upload it into a sql database.
It was created based on the following articles: 

https://www.dataquest.io/blog/loading-data-into-postgres/
https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
https://pynative.com/python-postgresql-tutorial/

## TLDR
Preparations:
* prepare a python virtual environment installing the requirements as listed in requirements.txt using e.g. virtualenv

To install the virtualenv package
```
$ pip install virtualenv
```

To setup a virtual environment, go to the project folder and open a terminal here. Do:
```
$ virtualenv database-env 
$ source database-env/bin/activate
```

Then go through the following steps to fill a postgresql database with python:
* store the .csv file in the /data folder
* adjust the input variables in the main.py script
* run a postgres database in a docker container (see section on postgres)
* run grafana in a docker container (see section on grafana)
* run `python main.py`

The script creates a table for each .csv file. Within each table an 'epoch' column is inserted, 
translating the text from the time column to an integer representing time in the unix epoch format.

To visualize in grafana:
* connect the database going through the grafana steps
* define the query using the query builder 
  * From: enter table name of choice e.g. "legSB_fore"
  * Time: search for "epoch"
  * Select: enter column name of choice e.g."S7 Leg SBFore Data Data Leg Load"
  * Where: remove the standard filter $__timeFilter

The sql query is as follows:
```
SELECT
  epoch AS "time",
  "[column name]"
FROM [table name]
ORDER BY 1
```

Once set up correctly you can add more queries to different tables as shown in the example below:

![Alt text](assets/grafana_example.png?raw=true "Grafana Example")

## postgres in a docker container
To pull the latest postgres docker image and spin up a database server in a container run:
```
$ docker run -p 5432:5432 -d --name postgres-database -e POSTGRES_PASSWORD=postgres postgres
```

Access to the database and the psql cli:
```
$ docker exec -it postgres-database /bin/bash 
$ su postgres psql
```

## grafana in a docker container
To pull the latest grafana docker image and spin up this service run:
```
$ docker run -d -p 3000:3000 grafana/grafana
```

### adding a postgres database in grafana
Choose postgresql as a datasource and fill in the following:
* host: docker container ip : port
* database: postgres
* user: postgres
* password: postgres
* disable TLS/SSL (its just for testing stuff on your own machine now...)

And finally save and test the connection to the database.

Note that if you are running postgres as a container the ip of the host is the ip of the docker container.
The default setting is to add containers to the "bridge" network.

To retreive the ip of the container containers on the bridge network:
```
$ docker network inspect bridge
```

### user permissions
The database user you specify when you add the data source should only be granted SELECT permissions on the specified database and tables you want to query. Now this is not the case, but it is ok for this use case.

Adding a user 'grafanareader' and granting read privileges on the 'public' schema and a table:
```
 CREATE USER grafanareader WITH PASSWORD 'password';
 GRANT USAGE ON SCHEMA public TO grafanareader;
 GRANT SELECT ON public.[table name] TO grafanareader;
```

Read more on setting permissions for a user here https://grafana.com/docs/grafana/latest/datasources/postgres/