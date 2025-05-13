import os
import psycopg2

conn = psycopg2.connect(host='postgres',
                        database='postgres',
                        user=os.environ["DB_USER"],
                        password=os.environ["DB_PASS"])

def get_db_cursor():
    return conn.cursor()

def commit():
    return conn.commit()

def rollback():
    return conn.rollback()
