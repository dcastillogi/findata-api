import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class DB:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=os.getenv("DATABASE_HOST"),
                user=os.getenv("DATABASE_USERNAME"),
                passwd=os.getenv("DATABASE_PASSWORD"),
                db=os.getenv("DATABASE"),
                ssl_verify_identity=True,
                autocommit=True,
                ssl={"ca": os.getenv("DATABASE_SSL_CA")}
            )
        except pymysql.Error as e:
            raise Exception(f"Database connection error: {e}")

    def reconnect(self):
        try:
            self.connection.ping(reconnect=True)
        except pymysql.Error as e:
            raise Exception(f"Database connection error: {e}")

    def __del__(self):
        self.connection.close()

    def insert(self, table, values):
        self.reconnect()
        try:
            with self.connection.cursor() as cursor:
                columns = ', '.join(values.keys())
                placeholders = ', '.join(['%s'] * len(values))
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, list(values.values()))
            return True
        except (pymysql.Error, Exception) as e:
            print("Error:", e)
            return False
        finally:
            cursor.close()

    def select(self, table, params=None):
        self.reconnect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table}", params)
                result = cursor.fetchall()
            return result
        except pymysql.Error as e:
            print("Error:", e)
            return False
