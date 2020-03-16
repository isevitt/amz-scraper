import pymysql
import dbconfig
import sys

class DBHelper:
    def connect(self):
        return pymysql.connect(host=dbconfig.host,
                               user=dbconfig.USERNAME,
                               passwd=dbconfig.PASS,
                               db=dbconfig.database)

    def get_all_unfinished(self):
        connection = self.connect()
        try:
            query = "SELECT * FROM heroku_08d3aef4493ede4.scraping_requests where is_finished = 0;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()
