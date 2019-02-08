""" This is a set of functions for use during the migration from block storage to object storage."""
import os
import boto3
from tqdm import tqdm

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url='https://nyc3.digitaloceanspaces.com',
    aws_access_key_id='K5TVKNCCT3FEU7KK3OJJ',
    aws_secret_access_key='3XN16jEOiOZoJ5b6FRhTwm7dIjJgxqm23wnKlE4+zMs',
)

client.upload_file(
    '/mnt/dzis/34d71e6e-016b-4500-9c89-c07770e7ab12-gam_des_008_003_080_002.jpg_files/13/18_1.jpeg',
    'archivo',
    '34d71e6e-016b-4500-9c89-c07770e7ab12-gam_des_008_003_080_002.jpg_files/13/18_1.jpeg',
    ExtraArgs={'ACL': 'public-read'},
)
