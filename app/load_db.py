#!/usr/bin/env python

import pymysql as mdb

class DB(object):
    connection = None
    cur = None

    def __init__(self):
        self.connection = mdb.connect(user="root", host="localhost", db="VoteSmart", charset='utf8')
        self.cur = self.connection.cursor()

    def query(self, query, params):
        return self.cur.execute(query, params)

    def __del__(self):
        self.connection.close()