''' database_adapter.py handles the connection to the database. '''
import os
import urlparse
import psycopg2

try:
    import components.local_database_data
except ImportError:
    print "local_database_data.py file is missing from components folder."
    print "Please create it manually"

def connect_db(is_for_deployment):
    ''' This function is used to establish the connection to the database according to the
    current environment. (local or Heroku or Travis)
    is_for_deployment parameter is used to determine if program is run in local or
    in Heroku '''
    connection = None

    if 'TRAVIS' in os.environ:
        connection = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='',
            host='localhost',
            port=''
        )
    elif is_for_deployment:
        # Specifying the postgres SQL and the database for Heroku
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        # Attempts to connect to the database and returns a connection object.
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    else:
        # Connects to the local postgres database
        connection = psycopg2.connect(
            database=components.local_database_data.get_database_name(),
            user=components.local_database_data.get_user_name(),
            password=components.local_database_data.get_password(),
            host=components.local_database_data.get_host_name(),
            port=components.local_database_data.get_port()
        )

    return connection
