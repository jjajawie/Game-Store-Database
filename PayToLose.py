import sqlite3

connection = sqlite3.connect('paytolose.sqlite')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        employee_SSN TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        DateOfBirth TEXT NOT NULL,
        StreetNumber INT NOT NULL,
        StreetName TEXT NOT NULL,
        City TEXT NOT NULL,
        State TEXT NOT NULL
        )''')

connection.commit
connection.close()