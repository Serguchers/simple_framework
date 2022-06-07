import sqlite3


connection = sqlite3.connect('test_base.sqlite')
curs = connection.cursor()
with open('db_scripts\db_creation.sql', 'r') as f:
    script = f.read()
curs.executescript(script)
curs.close()
connection.close()