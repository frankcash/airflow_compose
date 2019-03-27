# airflow_compose

A project for maintaining ETLs with Apache's Airflow.

## Running with Docker Compose

`docker-compose up --build`

## Running Locally

### Getting dependencies installed

```
cd /path/to/my/airflow_compose/
virtualenv -p `which python3` venv
source venv/bin/activate
```

From inside the virtualenv:
```
export SLUGIFY_USES_TEXT_UNIDECODE=yes
pip install -r requirements.txt
airflow initdb
```

### Running the web server

```
cd /path/to/my/airflow/workspace
source venv/bin/activate

export AIRFLOW_HOME=`pwd`/airflow_home
airflow webserver
```

### Running the scheduler

```
cd /path/to/my/airflow/workspace
export AIRFLOW_HOME=`pwd`/airflow_home

source venv/bin/activate
airflow scheduler
```

### Adding database
Go to the configuration tab underneath admin to add a database connection.


# Resources for Learning Apache Airflow

- http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/
- http://tech.marksblogg.com/airflow-postgres-redis-forex.html
- https://cloud.google.com/blog/products/gcp/how-to-aggregate-data-for-bigquery-using-apache-airflow
- https://www.dataengineeringpodcast.com/airflow-in-production-with-james-meickle-episode-43/
- https://www.astronomer.io/guides/dag-best-practices/
