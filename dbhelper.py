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


    def mark_as_finished(self, request_id):
        connection = self.connect()
        try:
            query = f"UPDATE heroku_08d3aef4493ede4.scraping_requests SET is_finished = 1 WHERE request_id = {request_id};"
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            print("finished query")
        except Exception as e:
            print(e)
        finally:
            connection.close()





