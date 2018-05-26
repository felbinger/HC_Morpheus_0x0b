#!/usr/bin/python

import pymysql.cursors

class MySQL:
    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname, dbchar):
        self.connection = pymysql.connect(host=dbhost,user=dbuser,password=dbpass,db=dbname,charset=dbchar,cursorclass=pymysql.cursors.DictCursor)
        self.connection.autocommit(True)
        
    # SELECT all rows
    def queryAll(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    # SELECT one row
    def query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()


    # INSERT, UPDATE, DELETE
    def update(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.lastrowid
