import mysql.connector
from contextlib import contextmanager

from mysql.connector import cursor
@contextmanager
def db_cur():
    mydb = None
    cursor = None
    try:
        mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="root",
                               database="flytau",
                               autocommit=True)
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
    with db_cur() as mycursor:
        mycursor.execute(query, arg)
        result = mycursor.fetchall()
    return result

def sql_insert(query,*arg):
    with db_cur() as mycursor:
        mycursor.execute(query, arg)

if __name__ == "__main__":
    pass