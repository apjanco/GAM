""" This is a set of functions for use during the migration from block storage to object storage."""
import os
import boto3
from tqdm import tqdm
import mysql.connector

cnx = mysql.connector.connect(user='gam_app', password=':3f^G;D<S,3b$Nt',
                              host='127.0.0.1',
                              database='os_migration')
cursor = cnx.cursor(buffered=True)

cnx1 = mysql.connector.connect(user='gam_app', password=':3f^G;D<S,3b$Nt',
                              host='127.0.0.1',
                              database='os_migration')
cursor1 = cnx1.cursor(buffered=True)

session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id='K5TVKNCCT3FEU7KK3OJJ',
                        aws_secret_access_key='3XN16jEOiOZoJ5b6FRhTwm7dIjJgxqm23wnKlE4+zMs')

def populate_db():
    for root, dirs, files in os.walk('/mnt/dzis/'):
        for filename in files:
            local_path = os.path.join(root, filename)
            query = ("INSERT os_migration.dzis (filename) VALUES ('%s')" % local_path)
            cursor.execute(query)
            cnx.commit()

def db_already_in_bucket(bucket):
    for key in client.list_objects(Bucket=bucket)['Contents']:
        path = '/mnt/dzis/' + key['Key']
        query = ("UPDATE os_migration.dzis SET copied = 1 WHERE filename LIKE '%s'" % path)
        cursor.execute(query)
        cnx.commit()


def calculate_total_files(path):
    counter = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            counter += 1
    print('total files= ', counter)
    return counter

def files_already_in_bucket(bucket):
    """Turns out that this isn't very useful. S3 only returns 1000 keys unless you create a loop over each key in the bucket"""
    files_in_bucket = []
    for key in client.list_objects(Bucket=bucket)['Contents']:
        files_in_bucket.append(key['Key'])
    files_in_bucket = set(files_in_bucket)
    return files_in_bucket

def copy_to_storage(path, bucket, total_files):
    """A function to copy all files in a given directory to object storage"""
    files_in_bucket = files_already_in_bucket(bucket)
    with tqdm(total=total_files) as pbar:
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename not in files_in_bucket:
                    local_path = os.path.join(root, filename)
                    client.upload_file(local_path, bucket, local_path.replace("/mnt/dzis/","" ), ExtraArgs={'ACL':'public-read'})
                    print(local_path.replace("/mnt/dzis/",""))
                    pbar.update(1)
                else:
                    pbar.update(1)

def db_to_storage(bucket):
    """A function to copy all files in the db to object storage."""
    with tqdm(total=total_files) as pbar:
        query = ("SELECT filename FROM os_migration.dzis WHERE copied IS NULL OR copied = 0")
        cursor.execute(query)
        for file in cursor:
            print(file[0])
            client.upload_file(file[0], bucket, file[0].replace("/mnt/dzis/","" ), ExtraArgs={'ACL':'public-read'})
            update_query = ("UPDATE os_migration.dzis SET copied = 1 WHERE filename LIKE '%s'" % file[0])
            cursor1.execute(update_query)
            cnx1.commit()
            pbar.update(1)

if __name__ == "__main__":
    bucket = 'gam-dzis'
    path = '/mnt/dzis'
    #total_files = 4425233

    total_files = calculate_total_files(path)
    #populate_db()
    #db_already_in_bucket(bucket)
    #db_to_storage(bucket)
    #already_in_bucket(bucket)
    #copy_to_storage(path, bucket,total_files)
