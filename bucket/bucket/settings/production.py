from .base import *
import dj_database_url

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

INTERNAL_IPS = ('127.0.0.1',)
