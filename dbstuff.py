#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('up4stuff.db')
print "Opened database successfully"

# PHONE          INT     NOT NULL UNIQUE,
conn.execute('''CREATE TABLE USERS
       (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
       PHONE          INT     NOT NULL,
       VERIFIED       INT     DEFAULT 0,
       COOKIEKEY      INT     DEFAULT 0,
       NAME           TEXT    );''')
print "Table created successfully"

conn.close()
