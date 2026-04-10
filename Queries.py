import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'paytolose.sqlite')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

def run_query(title, sql, params=()):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)
    cursor.execute(sql, params)
    columns = [d[0] for d in cursor.description]
    print("  " + " | ".join(columns))
    print("  " + "-" * 50)
    for row in cursor.fetchall():
        print("  " + " | ".join(str(v) for v in row))

run_query(
    "Q1: All Employees and Their Department",
    """
    SELECT e.Name, e.Position, e.HourlyRate, d.Dept_Name
    FROM EMPLOYEE e
    JOIN DEPARTMENT d ON e.Dept_ID = d.Dept_ID
    ORDER BY d.Dept_Name, e.Name
    """
)

run_query(
    "Q2: Titles with Publisher and Genres",
    """
    SELECT t.Name AS Title, p.Publisher_Name, GROUP_CONCAT(g.Genre_Name, ', ') AS Genres
    FROM TITLE t
    JOIN PUBLISHER p ON t.Publisher_ID = p.Publisher_ID
    JOIN CATEGORIZED_AS ca ON t.Title_ID = ca.Title_ID
    JOIN GENRE g ON ca.Genre_ID = g.Genre_ID
    GROUP BY t.Title_ID
    ORDER BY t.Name
    """
)

run_query(
    "Q3: Full Inventory List",
    """
    SELECT i.SKU, t.Name AS Title, i.Condition, i.Price
    FROM INVENTORY i
    JOIN TITLE t ON i.Title_ID = t.Title_ID
    ORDER BY t.Name, i.Condition
    """
)

run_query(
    "Q4: All Transactions with Employee and Customer",
    """
    SELECT tr.Transaction_ID, tr.Date, tr.TotalCost,
           e.Name AS Employee,
           CASE
               WHEN m.Customer_ID IS NOT NULL THEN 'Member'
               ELSE 'Guest'
           END AS Customer_Type,
           tr.Customer_ID
    FROM "TRANSACTIONS" tr
    JOIN EMPLOYEE e ON tr.Employee_SSN = e.SSN
    LEFT JOIN MEMBER m ON tr.Customer_ID = m.Customer_ID
    ORDER BY tr.Date
    """
)

run_query(
    "Q5: Total Sales Revenue Per Employee",
    """
    SELECT e.Name, COUNT(tr.Transaction_ID) AS Transactions, 
           ROUND(SUM(tr.TotalCost), 2) AS TotalRevenue
    FROM EMPLOYEE e
    JOIN "TRANSACTIONS" tr ON e.SSN = tr.Employee_SSN
    GROUP BY e.SSN
    ORDER BY TotalRevenue DESC
    """
)

run_query(
    "Q6: Members Ranked by Loyalty Points",
    """
    SELECT m.Customer_ID, m.EmailAddress, m.PhoneNum, m.Loyalty_Points
    FROM MEMBER m
    ORDER BY m.Loyalty_Points DESC
    """
)

run_query(
    "Q7: Titles and Their Available Platforms",
    """
    SELECT t.Name AS Title, GROUP_CONCAT(p.Platform_Name, ', ') AS Platforms
    FROM TITLE t
    JOIN AVAILABLE_ON ao ON t.Title_ID = ao.Title_ID
    JOIN PLATFORM p ON ao.Platform_ID = p.Platform_ID
    GROUP BY t.Title_ID
    ORDER BY t.Name
    """
)

run_query(
    "Q8: Checkout Items Per Transaction with Title",
    """
    SELECT ci.Transaction_ID, ci.Item_Num, t.Name AS Title,
           i.Condition, ci.Sale_Price
    FROM CHECKOUT_ITEMS ci
    JOIN INVENTORY i ON ci.SKU = i.SKU
    JOIN TITLE t ON i.Title_ID = t.Title_ID
    ORDER BY ci.Transaction_ID, ci.Item_Num
    """
)

run_query(
    "Q9: Best Selling Titles by Copies Sold",
    """
    SELECT t.Name AS Title, COUNT(ci.SKU) AS CopiesSold,
           ROUND(SUM(ci.Sale_Price), 2) AS TotalRevenue
    FROM CHECKOUT_ITEMS ci
    JOIN INVENTORY i ON ci.SKU = i.SKU
    JOIN TITLE t ON i.Title_ID = t.Title_ID
    GROUP BY t.Title_ID
    ORDER BY CopiesSold DESC
    """
)

run_query(
    "Q10: Departments with Manager and Budget",
    """
    SELECT d.Dept_Name, e.Name AS Manager, d.Budget
    FROM DEPARTMENT d
    JOIN EMPLOYEE e ON d.Manager_SSN = e.SSN
    ORDER BY d.Budget DESC
    """
)

connection.close()