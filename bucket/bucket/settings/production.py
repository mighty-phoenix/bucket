from .base import *
import dj_database_url

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

INTERNAL_IPS = ('127.0.0.1',)
