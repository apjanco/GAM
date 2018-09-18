import boto3
import botocore
import ast
from gam_app.models import Imagen
from archivo.settings_secret import SECRET_ACCESS_KEY, ACCESS_KEY_ID


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
                                 aws_secret_access_key = SECRET_ACCESS_KEY, #'siqMTLrCUcjwCXLG3HUa+2CGTuETrQRyiqsfHayHcI',
                                 aws_access_key_id = ACCESS_KEY_ID) #'XWVILRP2O4XT5WXK6BHK')

        bags = []
        for thing in client.list_objects(Bucket='bolsas')['Contents']:
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
