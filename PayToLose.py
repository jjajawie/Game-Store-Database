import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'paytolose.sqlite')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS DEPARTMENT (
        Dept_ID     INTEGER PRIMARY KEY,
        Dept_Name   TEXT    NOT NULL,
        Budget      REAL    NOT NULL,
        Manager_SSN TEXT            
    );
""")
 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS EMPLOYEE (
        SSN          TEXT PRIMARY KEY,
        Name         TEXT NOT NULL,
        DateOfBirth  TEXT NOT NULL,
        StreetNumber TEXT NOT NULL,
        StreetName   TEXT NOT NULL,
        City         TEXT NOT NULL,
        State        TEXT NOT NULL,
        Position     TEXT NOT NULL,
        HourlyRate   REAL NOT NULL,
        PhoneNum     TEXT NOT NULL,
        Dept_ID      INTEGER NOT NULL,
        FOREIGN KEY (Dept_ID) REFERENCES DEPARTMENT(Dept_ID)
    );
""")
 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PUBLISHER (
        Publisher_ID   INTEGER PRIMARY KEY,
        Publisher_Name TEXT NOT NULL,
        emailAddress   TEXT,
        PhoneNumber    TEXT
    );
""")
 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS TITLE (
        Title_ID     INTEGER PRIMARY KEY,
        Name         TEXT    NOT NULL,
        Description  TEXT,
        Release_Date TEXT,
        Publisher_ID INTEGER NOT NULL,
        FOREIGN KEY (Publisher_ID) REFERENCES PUBLISHER(Publisher_ID)
    );
""")
 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS GENRE (
        Genre_ID   INTEGER PRIMARY KEY,
        Genre_Name TEXT NOT NULL
    );
""")
 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS PLATFORM (
        Platform_ID   INTEGER PRIMARY KEY,
        Platform_Name TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CATEGORIZED_AS (
        Title_ID  INTEGER NOT NULL,
        Genre_ID  INTEGER NOT NULL,
        PRIMARY KEY (Title_ID, Genre_ID),
        FOREIGN KEY (Title_ID)  REFERENCES TITLE(Title_ID),
        FOREIGN KEY (Genre_ID)  REFERENCES GENRE(Genre_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS AVAILABLE_ON (
        Title_ID    INTEGER NOT NULL,
        Platform_ID INTEGER NOT NULL,
        PRIMARY KEY (Title_ID, Platform_ID),
        FOREIGN KEY (Title_ID)    REFERENCES TITLE(Title_ID),
        FOREIGN KEY (Platform_ID) REFERENCES PLATFORM(Platform_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS INVENTORY (
        SKU       TEXT    PRIMARY KEY,
        Price     REAL    NOT NULL,
        Condition TEXT    NOT NULL,
        Title_ID  INTEGER NOT NULL,
        FOREIGN KEY (Title_ID) REFERENCES TITLE(Title_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMER (
        Customer_ID INTEGER PRIMARY KEY
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS MEMBER (
        Customer_ID    INTEGER PRIMARY KEY,
        Join_Date      TEXT,
        EmailAddress   TEXT,
        PhoneNum       TEXT,
        Loyalty_Points INTEGER DEFAULT 0,
        FOREIGN KEY (Customer_ID) REFERENCES CUSTOMER(Customer_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS GUEST (
        Customer_ID INTEGER PRIMARY KEY,
        FOREIGN KEY (Customer_ID) REFERENCES CUSTOMER(Customer_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS TRANSACTIONS (
        Transaction_ID INTEGER PRIMARY KEY,
        Date           TEXT    NOT NULL,
        TotalCost      REAL    NOT NULL,
        Employee_SSN   TEXT    NOT NULL,
        Customer_ID    INTEGER NOT NULL,
        FOREIGN KEY (Employee_SSN) REFERENCES EMPLOYEE(SSN),
        FOREIGN KEY (Customer_ID)  REFERENCES CUSTOMER(Customer_ID)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS CHECKOUT_ITEMS (
        Transaction_ID INTEGER NOT NULL,
        Item_Num       INTEGER NOT NULL,
        SKU            TEXT    NOT NULL,
        Sale_Price     REAL    NOT NULL,
        PRIMARY KEY (Transaction_ID, Item_Num),
        FOREIGN KEY (Transaction_ID) REFERENCES TRANSACTIONS(Transaction_ID),
        FOREIGN KEY (SKU)            REFERENCES INVENTORY(SKU)
    );
""")
 
cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS fk_dept_manager
    BEFORE INSERT ON DEPARTMENT
    FOR EACH ROW
    WHEN NEW.Manager_SSN IS NOT NULL
    BEGIN
        SELECT RAISE(ABORT, 'Foreign key violation: Manager_SSN not in EMPLOYEE')
        WHERE NOT EXISTS (
            SELECT 1 FROM EMPLOYEE WHERE SSN = NEW.Manager_SSN
        );
    END;
""")

connection.commit()
connection.close()