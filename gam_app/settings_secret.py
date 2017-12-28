import os 

SECRET_KEY = 'tyn^ej@zls1p5k$g*=!nm(v6evifm-au_esy)#(d=5&*fo#r80'

API_KEY = 'AIzaSyBZZcmX_W0rFAJUmHbLnQyOGOxJqdm902w'


AWS_ACCESS_KEY_ID = 'K5TVKNCCT3FEU7KK3OJJ'
AWS_SECRET_ACCESS_KEY = '3XN16jEOiOZoJ5b6FRhTwm7dIjJgxqm23wnKlE4+zMs'
AWS_STORAGE_BUCKET_NAME = 'archivo'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'


STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

