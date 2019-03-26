from datetime import datetime
from airflow.models import DAG
from postgres_to_s3_operator import PostgresToS3Operator # https://stackoverflow.com/questions/43907813/cant-import-airflow-plugins

dag = DAG('hackerqueue_etl_dag_v0_0_1',
    description='etl_hackerqueue_info_once_a_day',
    schedule_interval='0 12 * * *',
    start_date=datetime(2019, 3, 26), catchup=False)

export = PostgresToS3Operator(task_id="hackerqueue_export_task", dag=dag, postgres_conn_id ="hackerqueue_prod", s3_conn_id = 'demo_bucket', query="SELECT story_url, source, title, comments FROM public.crawls;")

export