import boto3
import pandas as pd
import psycopg2
import json
import configparser

config = configparser.ConfigParser()
config.read_file(open('./dwh.cfg'))


KEY = config.get('AWS','KEY')
SECRET = config.get('AWS','SECRET')
DWH_CLUSTER_TYPE = config.get('DWH','DWH_CLUSTER_TYPE')
DWH_NUM_NODES = config.get('DWH','DWH_NUM_NODES')
DWH_NODE_TYPE = config.get('DWH','DWH_NODE_TYPE')
DWH_CLUSTER_IDENTIFIER =  config.get('DWH','DWH_CLUSTER_IDENTIFIER')
DWH_DB = config.get('DWH','DWH_DB')
DWH_DB_USER = config.get('DWH','DWH_DB_USER')
DWH_DB_PASSWORD = config.get('DWH','DWH_DB_PASSWORD')
DWH_PORT = config.get('DWH','DWH_PORT')
DWH_IAM_ROLE_NAME = config.get('DWH','DWH_IAM_ROLE_NAME')

print(DWH_DB_USER,DWH_DB_PASSWORD,DWH_PORT,DWH_DB)

redshift = boto3.client('redshift',
                        region_name='ap-south-1',
                        aws_access_key_id =KEY,
                        aws_secret_access_key = SECRET
                        )

iam = boto3.client('iam',
                   aws_access_key_id =KEY,
                   aws_secret_access_key = SECRET,
                   region_name = 'ap-south-1',
                   )

try:
    response = redshift.create_cluster(ClusterType=DWH_CLUSTER_TYPE,
                            NodeType =DWH_NODE_TYPE,
                            DBName=DWH_DB,
                            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
                            MasterUsername=DWH_DB_USER,
                            MasterUserPassword= DWH_DB_PASSWORD
                                       )

    print(redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER))
except Exception as e:
    print(e)

