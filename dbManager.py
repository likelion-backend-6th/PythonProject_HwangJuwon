import psycopg2


class DB:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        dbname='library',
        user='postgres',
        password='1234'
    )
    cur = conn.cursor()