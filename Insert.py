import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'paytolose.sqlite')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executemany("""
    INSERT OR IGNORE INTO DEPARTMENT (Dept_ID, Dept_Name, Budget, Manager_SSN)
    VALUES (?, ?, ?, NULL)
""", [
    (1, 'Sales',      50000.00),
    (2, 'Inventory',  30000.00),
    (3, 'Management', 70000.00),
])

cursor.executemany("""
    INSERT OR IGNORE INTO EMPLOYEE (SSN, Name, DateOfBirth, StreetNumber, StreetName, City, State, Position, HourlyRate, PhoneNum, Dept_ID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ('111-22-3333', 'Alice Johnson', '1990-04-12', '101', 'Maple St',   'Macomb',    'MI', 'Sales Associate', 15.00, '734-555-0101', 1),
    ('222-33-4444', 'Bob Smith',     '1985-07-23', '202', 'Oak Ave',    'Dearborn',    'MI', 'Sales Associate', 15.50, '734-555-0102', 1),
    ('333-44-5555', 'Carol White',   '1992-01-05', '303', 'Grandma Rd',    'Toledo',    'OH', 'Inventory Clerk', 14.00, '419-555-0103', 2),
    ('444-55-6666', 'David Brown',   '1980-11-30', '404', 'Ridge Blvd',   'Madison Heights',    'MI', 'Inventory Clerk', 14.50, '734-555-0104', 2),
    ('555-66-7777', 'Eva Martinez',  '1978-03-18', '505', 'Monkey Ln',   'Ann Arbor', 'MI', 'Store Manager',   22.00, '734-555-0105', 3),
    ('666-77-8888', 'Frank Lee',     '1983-09-09', '606', 'Cow Dr',   'Monroe',    'MI', 'Dept Manager',    20.00, '734-555-0106', 1),
    ('777-88-9999', 'Grace Kim',     '1995-06-14', '707', 'Cat Way', 'Toledo',    'OH', 'Dept Manager',    19.00, '419-555-0107', 2),
])

cursor.execute("UPDATE DEPARTMENT SET Manager_SSN = '555-66-7777' WHERE Dept_ID = 3;")
cursor.execute("UPDATE DEPARTMENT SET Manager_SSN = '666-77-8888' WHERE Dept_ID = 1;")
cursor.execute("UPDATE DEPARTMENT SET Manager_SSN = '777-88-9999' WHERE Dept_ID = 2;")

cursor.executemany("""
    INSERT OR IGNORE INTO PUBLISHER (Publisher_ID, Publisher_Name, emailAddress, PhoneNumber)
    VALUES (?, ?, ?, ?)
""", [
    (1, 'Nintendo',          'contact@nintendo.com',    '800-123-1233'),
    (2, 'Sony Interactive',  'support@playstation.com', '800-234-2344'),
    (3, 'Xbox Game Studios', 'support@xbox.com',        '800-469-4696'),
    (4, 'Capcom',            'info@capcom.com',         '800-225-5555'),
    (5, 'Bandai Namco',      'info@bandainamco.com',    '800-963-1111'),
])

cursor.executemany("""
    INSERT OR IGNORE INTO TITLE (Title_ID, Name, Description, Release_Date, Publisher_ID)
    VALUES (?, ?, ?, ?, ?)
""", [
    (1, 'The Legend of Zelda: Breath of the Wild', 'Open world adventure.',        '2017-03-03', 1),
    (2, 'God of War',                              'Norse mythology action.',       '2018-04-20', 2),
    (3, 'Halo Infinite',                           'Sci-fi shooter.',       '2021-12-08', 3),
    (4, 'Monster Hunter Rise',                     'Hunt monsters in Japan.',     '2021-03-26', 4),
    (5, 'Elden Ring',                              'dark fantasy RPG.',       '2022-02-25', 5),
    (6, 'Super Mario Odyssey',                     'open world platformer.', '2017-10-27', 1),
    (7, 'Spider-Man: Miles Morales',               'Superhero action adventure.',        '2020-11-12', 2),
])

cursor.executemany("""
    INSERT OR IGNORE INTO GENRE (Genre_ID, Genre_Name)
    VALUES (?, ?)
""", [
    (1, 'Action'),
    (2, 'Adventure'),
    (3, 'RPG'),
    (4, 'Shooter'),
    (5, 'Platformer'),
])

cursor.executemany("""
    INSERT OR IGNORE INTO PLATFORM (Platform_ID, Platform_Name)
    VALUES (?, ?)
""", [
    (1, 'Nintendo Switch'),
    (2, 'PlayStation 4'),
    (3, 'PlayStation 5'),
    (4, 'Xbox Series X'),
    (5, 'PC'),
])

cursor.executemany("""
    INSERT OR IGNORE INTO CATEGORIZED_AS (Title_ID, Genre_ID)
    VALUES (?, ?)
""", [
    (1, 1), (1, 2),
    (2, 1),
    (3, 1), (3, 4),
    (4, 1), (4, 3),
    (5, 2), (5, 3),
    (6, 2), (6, 5),
    (7, 1), (7, 2),
])

cursor.executemany("""
    INSERT OR IGNORE INTO AVAILABLE_ON (Title_ID, Platform_ID)
    VALUES (?, ?)
""", [
    (1, 1),
    (2, 2), (2, 3),
    (3, 4), (3, 5),
    (4, 1), (4, 5),
    (5, 2), (5, 3), (5, 4), (5, 5),
    (6, 1),
    (7, 2), (7, 3),
])

cursor.executemany("""
    INSERT OR IGNORE INTO INVENTORY (SKU, Price, Condition, Title_ID)
    VALUES (?, ?, ?, ?)
""", [
    ('SKU-001', 59.99, 'New',  1),
    ('SKU-002', 39.99, 'Used', 1),
    ('SKU-003', 49.99, 'New',  2),
    ('SKU-004', 29.99, 'Used', 2),
    ('SKU-005', 54.99, 'New',  3),
    ('SKU-006', 59.99, 'New',  4),
    ('SKU-007', 44.99, 'Used', 4),
    ('SKU-008', 64.99, 'New',  5),
    ('SKU-009', 49.99, 'Used', 5),
    ('SKU-010', 49.99, 'New',  6),
    ('SKU-011', 34.99, 'Used', 6),
    ('SKU-012', 59.99, 'New',  7),
    ('SKU-013', 44.99, 'Used', 7),
])

cursor.executemany("""
    INSERT OR IGNORE INTO CUSTOMER (Customer_ID) VALUES (?)
""", [(1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,)])

cursor.executemany("""
    INSERT OR IGNORE INTO MEMBER (Customer_ID, Join_Date, EmailAddress, PhoneNum, Loyalty_Points)
    VALUES (?, ?, ?, ?, ?)
""", [
    (1, '2021-06-01', 'jdoe@gmail.com',    '734-555-1001', 320),
    (2, '2020-11-15', 'supersmith@outlook.com',  '734-555-1002', 150),
    (3, '2022-03-22', 'mjonesbossman@yahoo.com',  '419-555-1003', 540),
    (4, '2019-08-30', 'lwilsonradio@gmail.com', '734-555-1004', 800),
    (5, '2023-01-10', 'amazingtaylor@icloud.com', '734-555-1005',  90),
])

cursor.executemany("""
    INSERT OR IGNORE INTO GUEST (Customer_ID) VALUES (?)
""", [(6,),(7,),(8,)])

cursor.executemany("""
    INSERT OR IGNORE INTO "TRANSACTIONS" (Transaction_ID, Date, TotalCost, Employee_SSN, Customer_ID)
    VALUES (?, ?, ?, ?, ?)
""", [
    (1,  '2024-01-05',  59.99, '111-22-3333', 1),
    (2,  '2024-01-07',  79.98, '111-22-3333', 2),
    (3,  '2024-01-10',  49.99, '222-33-4444', 6),
    (4,  '2024-01-12',  94.98, '222-33-4444', 3),
    (5,  '2024-01-15',  64.99, '111-22-3333', 4),
    (6,  '2024-02-01',  44.99, '222-33-4444', 7),
    (7,  '2024-02-03',  59.99, '111-22-3333', 5),
    (8,  '2024-02-10', 109.98, '222-33-4444', 1),
    (9,  '2024-02-14',  34.99, '111-22-3333', 8),
    (10, '2024-03-01',  59.99, '222-33-4444', 2),
])

cursor.executemany("""
    INSERT OR IGNORE INTO CHECKOUT_ITEMS (Transaction_ID, Item_Num, SKU, Sale_Price)
    VALUES (?, ?, ?, ?)
""", [
    (1,  1, 'SKU-001', 59.99),
    (2,  1, 'SKU-003', 49.99),
    (2,  2, 'SKU-011', 29.99),
    (3,  1, 'SKU-005', 49.99),
    (4,  1, 'SKU-008', 64.99),
    (4,  2, 'SKU-004', 29.99),
    (5,  1, 'SKU-012', 64.99),
    (6,  1, 'SKU-007', 44.99),
    (7,  1, 'SKU-006', 59.99),
    (8,  1, 'SKU-002', 39.99),
    (8,  2, 'SKU-009', 49.99),
    (8,  3, 'SKU-013', 19.99),
    (9,  1, 'SKU-011', 34.99),
    (10, 1, 'SKU-001', 59.99),
])

connection.commit()
connection.close()