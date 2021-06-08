# database-setup

This code imports data from a .csv, stores it in a pandas dataframe to upload it to a sql database.
It was created based on the following articles: 

https://www.dataquest.io/blog/loading-data-into-postgres/
https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
https://pynative.com/python-postgresql-tutorial/



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