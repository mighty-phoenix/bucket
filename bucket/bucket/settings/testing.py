from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

INSTALLED_APPS += (
    'django_nose',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bucketdb',
        'USER': 'payal',
        'PASSWORD': 'ikon',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'bucket.bucket.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nocapture',
    '--nologcapture',
    # '--with-doctest',
    # '--doctest-options=+ELLIPSIS',
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
