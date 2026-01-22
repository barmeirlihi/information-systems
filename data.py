import mysql.connector
from contextlib import contextmanager
import os

from mysql.connector import cursor
@contextmanager
def db_cur():
    mydb = None
    cursor = None
    try:
        DB_HOST = os.environ.get("DB_HOST", "awseb-e-a3qj6ivcmk-stack-awsebrdsdatabase-noappqk8etts.c14secq48pc3.il-central-1.rds.amazonaws.com")
        DB_USER = os.environ.get("DB_USER", "flytau48")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "fly48tau!")
        DB_NAME=os.environ.get("DB_NAME", "ebdb")
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=True,
            connection_timeout=10,
            connect_timeout=10
        )
        cursor = mydb.cursor(buffered=True)
        yield cursor
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()


def sql_query(query,*arg):
    try:
        with db_cur() as mycursor:
            mycursor.execute(query, arg)
            result = mycursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        raise
    except Exception as e:
        print(f"Unexpected error in sql_query: {e}")
        raise

def sql_insert(query,*arg):
    with db_cur() as mycursor:
        mycursor.execute(query, arg)

if __name__ == "__main__":
    pass