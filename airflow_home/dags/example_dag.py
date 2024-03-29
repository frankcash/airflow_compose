from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.version import version
from datetime import datetime, timedelta


def my_custom_function(ts,**kwargs):
    """
    This can be any python code you want and is called from the python operator. The code is not executed until
    the task is run by the airflow scheduler.
    """
    print(f"I am task number {kwargs['task_number']}. This DAG Run execution date is {ts} and the current time is {datetime.now()}")
    print('Here is the full DAG Run context. It is available because provide_context=True')
    print(kwargs)


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
with DAG('example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=timedelta(minutes=30),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
         default_args=default_args,
         catchup=False # enable if you don't want historical dag runs to run
         ) as dag:


        tn = PythonOperator(
            task_id=f'python_print_date',
            python_callable=my_custom_function,
            op_kwargs={'task_number': 0},
        )