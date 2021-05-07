from app import create_app
from os import path, environ

app = create_app('PRODUCTION')

print(environ.get('secret_key'))