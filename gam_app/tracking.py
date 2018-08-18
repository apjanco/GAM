import boto3
import botocore
import ast
from gam_app.models import Imagen

### from https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
### Handles times when network hangs or no reponse from Digital Ocean
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)
###


def getBags():
    try:
        signal.alarm(5)
        session = boto3.session.Session()
        client = session.client('s3',
                                 endpoint_url = 'https://nyc3.digitaloceanspaces.com',
                                 aws_secret_access_key = '3XN16jEOiOZoJ5b6FRhTwm7dIjJgxqm23wnKlE4+zMs',
                                 aws_access_key_id = 'K5TVKNCCT3FEU7KK3OJJ')

        bags = []
        for thing in client.list_objects(Bucket='ds-gam')['Contents']:
            if '.zip' in thing['Key']:
                bags += [thing['Key'][:-4].replace('Bags/','')]
            else:
                pass
        with open('/tmp/bag_temp.txt', 'w') as f:
            f.write(str(bags))
            f.close()
        return bags

    except TimeoutException:
        with open('/tmp/bag_temp.txt', 'r') as f:
            bags = f.read()
            bags = ast.literal_eval(bags)
        return sorted(bags)

    except botocore.exceptions.ClientError:
        with open('/tmp/bag_temp.txt', 'r') as f:
            bags = f.read()
            bags = ast.literal_eval(bags)
        return sorted(bags)

def getImportedBags():
    bags = []
    for imagen in Imagen.objects.all():
        bags += [imagen.bag_name]
    return bags
