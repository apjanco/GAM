import os
import boto3
import botocore
import ast
from gam_app.models import Imagen
from archivo.settings_secret import SECRET_ACCESS_KEY, ACCESS_KEY_ID, AWS_SECRET_KEY, AWS_KEY
import getpass


def aws_client(session):

    client = session.client('s3',
                            endpoint_url='https://s3.amazonaws.com',
                            aws_secret_access_key=AWS_SECRET_KEY,
                            aws_access_key_id=AWS_KEY,
                            )
    return client


def do_client(session):
    client = session.client('s3',
                            endpoint_url = 'https://nyc3.digitaloceanspaces.com',
                            aws_secret_access_key = SECRET_ACCESS_KEY,
                            aws_access_key_id = ACCESS_KEY_ID)
    return client
### from https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
### Handles times when network hangs or no reponse from Digital Ocean
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
#signal.signal(signal.SIGALRM, timeout_handler)
###


def descargar_una_sola_bolsa(filename):
    """This is a function used to download individual bag files from object storage"""
    try:
        config = botocore.client.Config(connect_timeout=2000, read_timeout=2000)
        session = boto3.session.Session()
        client = aws_client(session)

        #client.download_file('bolsas', filename, '/mnt/bags/{}'.format(filename))
        client.download_file('gam-bolsas', filename, '/mnt/bags/{}'.format(filename))

        return True

    except Exception as e:
        print(e)


def descargar_una_sola_bolsa_s3cmd(filename):
    getpass.getuser()
    os.system('s3cmd get "s3://bolsas/{}" /tmp/{}'.format(filename, filename))
    return True


def getBags():
    try:
        # signal.alarm(5)
        session = boto3.session.Session()
        client = aws_client(session)

        bags = []
        for thing in client.list_objects(Bucket='gam-bolsas')['Contents']:
            if '.zip' in thing['Key']:
                bags += [thing['Key'][:-4].replace('Bags/','')]
            else:
                pass
        with open('/tmp/bag_temp.txt', 'w+') as f:
            f.write(str(bags))
            f.close()
        return bags

    except TimeoutException:
        with open('/tmp/bag_temp.txt', 'r+') as f:
            bags = f.read()
            bags = ast.literal_eval(bags)
        return sorted(bags)

    except botocore.exceptions.ClientError:
        with open('/tmp/bag_temp.txt', 'r+') as f:
            bags = f.read()
            bags = ast.literal_eval(bags)
        return sorted(bags)

    except KeyError:
        with open('/tmp/bag_temp.txt', 'r') as f:
            bags = f.read()
            bags = ast.literal_eval(bags)
        return sorted(bags)

def getImportedBags():
    bags = []
    for imagen in Imagen.objects.all():
        bags += [imagen.bag_name]
    return bags
