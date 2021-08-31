from airflow import DAG

from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


def my_custom_function(**kwargs):
    es = ElasticsearchHook(elasticsearch_conn_id='production-es')
    es_conn = es.get_conn()
    tables = es_conn.execute('SHOW TABLES')
    for table, *_ in tables:
        print(f"table: {table}")
        rows = es_conn.execute(f'SELECT COUNT(*) FROM {table}')
        print([row for row in rows])

    

    return


# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('elasticsearch_dag',
         start_date=datetime(2021, 8, 30),
         max_active_runs=1,
         schedule_interval=timedelta(days=1),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:


        tn = PythonOperator(
            task_id=f'python_print_date',
            python_callable=my_custom_function,
            op_kwargs={'task_number': 0},
        )