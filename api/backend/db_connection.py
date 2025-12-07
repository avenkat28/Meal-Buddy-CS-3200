import os
from flask import g
import pymysql

class DB:
    def __init__(self):
        self.conn = None

    def connect(self):
        """Create database connection"""
        self.conn = pymysql.connect(
            host=os.getenv('DB_HOST', 'db'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('MYSQL_ROOT_PASSWORD', 'your_password'),
            database=os.getenv('DB_NAME', 'mealbuddy'),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        return self.conn

    def get_db(self):
        """Get database connection, create if doesn't exist"""
        if 'db_conn' not in g:
            g.db_conn = self.connect()
        return g.db_conn

    def close_db(self, e=None):
        """Close database connection"""
        db_conn = g.pop('db_conn', None)
        if db_conn is not None:
            db_conn.close()

# Create single instance
db = DB()
