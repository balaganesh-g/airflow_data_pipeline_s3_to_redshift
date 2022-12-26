from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from textwrap import dedent

dag_args = {
    'owner': 'bala',
    'start_date': datetime.now(),
    'email': ['bala@yopmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_toll_data',
    default_args=dag_args,
    description='Apache Airflow poc',
    schedule_interval=timedelta(days=1),
    dagrun_timeout=timedelta(minutes=60)
)

url ='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz'


unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command=f'sudo wget {url} && tar zxvf tolldata.tgz -C ./data',
    dag=dag,
    run_as_user = 'root'
)

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1,2,3,4 ./data/vehicle-data.csv > ./data/csv_data.csv',
    dag=dag,
)

extract_data_from_tsv=BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5,6,7 ./data/tollplaza-data.tsv > ./data/tsv_data.csv',
    dag=dag,
)

extract_data_from_fixed_width=BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -b 58-67 < ./data/payment-data.txt > ./data/fixed_width_data.csv',
    dag=dag,
)


consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d, ./data/csv_data.csv ./data/tsv_data.csv ./data/fixed_width_data.csv > ./data/extracted_data.csv',
    dag=dag,
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command='cut -d, -f4 ./data/extracted_data.csv | tr "[a-z]" "[A-Z]" > ./data/transformed_data.csv',
    dag=dag,
    run_as_user = 'root'
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
