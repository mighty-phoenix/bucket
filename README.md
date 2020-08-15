# bucket

## Setup for Windows

1. Make sure you have installed Python 3.6 or newer, make sure you have the right one (32/64 bits). [Source](https://www.python.org/downloads/). During installation please pay attention to the following details :
* Tick/Select Add Python 3.6 to PATH
* Select Customize Installation (this is important)
* Tick/Select pip (others, leave as default), this is important
* Tick install for all users
* Tick add Python to environment variables
* Tick create shortcuts for installed applications
* Precomplie standard libary
* Select install location and hit install

1. Run `pip install virtualenv` using windows command line
1. You would have to install PostgreSQL. Download from [official location](https://www.postgresql.org/download/windows/) or alternative location, you could lookup some PostgreSQL tutorials online if you are completely blank on this. 
1. Fork and clone the repo, and cd into the `bucket` directory.  Use git CMD or git Bash(unix-like terminal) to do so.
1. Create a virtual environment with Python 3 and install dependencies, using CMD :
 
     ```bash
     $ virtualenv venv
     $ ./venv/Scripts/activate
     $ pip install -r requirements.txt 
     ```
1. Create `bucketdb` database, where `bucketdb` might be any suitable name.
- Open the SQL Shell for postgresql from the windows start menu or wherever accessible

    ```
    $ Server [localhost]:  Just press enter, leave this empty
    $ Database [postgres]: Just press enter, leave this empty
    $ Port [5432]: This is the default port just press enter, leave this empty
    $ Username [postgres]: This is the default username just press enter, leave this empty
    $ Password for user postgres: Input password you created during installation and press enter
    $ CREATE USER <anyname you want e.g bucket> WITH PASSWORD 'your password';
    $ CREATE DATABASE bucketdb;
    $ \c bucketdb;
    $ GRANT ALL PRIVILEGES ON bucketdb TO <username created above>;
    ```
1. Fill in the database details in `bucket/bucket/settings/dev.py`.
1. Run `git update-index --assume-unchanged bucket/manage.py bucket/bucket/wsgi.py`. In `manage.py` and `wsgi.py` change `'bucket.settings.production'` to `'bucket.settings.dev'`. 
1. Run `set SECRET_KEY=foobarbaz` in your terminal, ideally the secret key
  should be 40 characters long, unique and unpredictable. 
1. You will need a TMDB API key, which you can register and get from [here](https://developers.themoviedb.org/3). Run `set TMDB_API_KEY=apikey` in your terminal.
1. Add both the keys to your virtualenv's activate file.
1. Run `python bucket/manage.py migrate`.
1. Run `python bucket/manage.py createsuperuser` to create a superuser for the admin panel.
  Fill in the details asked.
1. Run `python bucket/manage.py runserver` to start the development server. When in testing
  or production, feed the respective settings file from the command line, e.g. for
  testing `python bucket/manage.py runserver --settings=bucket.settings.testing`.
1. Run `python bucket/manage.py test --settings=bucket.settings.testing`
  to run all the tests.
