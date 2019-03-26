import logging
import os
import unicodecsv as csv
import io
import uuid
from datetime import timedelta, datetime
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from airflow.hooks import PostgresHook, S3Hook


logger = logging.getLogger(__name__)
airflow_path = os.environ["AIRFLOW_HOME"]


class PostgresToS3Operator(BaseOperator):
    @apply_defaults
    def __init__(self, postgres_conn_id, s3_conn_id, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.s3_conn_id = s3_conn_id
        self.query = query

    def execute(self, context):
        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        s3_hook = S3Hook(aws_conn_id=self.s3_conn_id)
        res = self.query_db(self.query, postgres_hook)
        res.seek(0)
        s3_hook.load_file_obj(res, key="egress/sources.airflow.csv", bucket_name="demo-bucket-temp-977338899", replace=True)
        return True
    
    def query_db(self, query, hook):
        content = hook.get_records(sql=query)
        return self.gen_file(content)
   
    def gen_file(self, content):
        print(f"gen_file {content}")
        output = io.BytesIO()
        writer = csv.writer(output, delimiter='|', encoding='utf-8')
        writer.writerows(content)
        return output

    def cleanup(self, fname):
        os.remove(fname)


class PostgresToS3Operators(AirflowPlugin):
    name = "postgres_to_s3_operator"
    operators = [PostgresToS3Operator]