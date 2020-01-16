import sqlite3
import os

class Db_connection:
    database_filename = "./database/tic_tac_toe.db"

    @staticmethod
    def check_database_connection():
        return os.path.isfile(Db_connection.database_filename)

    @staticmethod
    def query(query):
        if not Db_connection.check_database_connection():
            raise Exception("Couldn't connect to database")
        
        connection = sqlite3.connect(Db_connection.database_filename)
        result = connection.execute(query)
        result = result.fetchall()
        connection.commit()
        
        if query.split(" ")[0].lower() == "insert":
            result = connection.execute("SELECT last_insert_rowid()")
            result = result.fetchall()

        connection.close()

        return result
