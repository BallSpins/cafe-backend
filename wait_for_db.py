import time
import os
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    raise ValueError('DATABASE_URL not found in environment variables')

parsed = urlparse(db_url)

host = parsed.hostname or 'localhost'
port = parsed.port or 3306
user = parsed.username
password = parsed.password
database = parsed.path.lstrip('/') if parsed.path else None

while True:
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print('MySQL is ready.')
            break
    except Error as e:
        print('Waiting for MySQL...')
        time.sleep(1)
