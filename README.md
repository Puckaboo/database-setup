# database-setup

This code imports data from a .csv, stores it in a pandas dataframe to upload it to a sql database.
It was created based on the following articles: 

https://www.dataquest.io/blog/loading-data-into-postgres/
https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/


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