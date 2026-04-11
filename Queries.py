import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'paytolose.sqlite')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

while True:
    print("1. List Dept Managers")
    print("2. Show Used Inventory")
    print("3. Show Employees making $20 or more")
    print("4. Change Loyalty Member Email")
    print("5. Put Item on Sale")
    print("6. List Employees by Sales (Ascending)")
    print("7. Give Raise to Inventory Dept")
    print("8. Remove Member")
    print("9. Hire New Employee")
    print("10. Best Selling Titles")
    print("0. Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":
        cursor.execute("SELECT Dept_name, Name FROM DEPARTMENT JOIN EMPLOYEE ON Manager_SSN = SSN")
        results = cursor.fetchall()
        print("Department | Name")
        for row in results:
            print(row)

    elif choice == "2":
        cursor.execute("""SELECT TITLE.Name, INVENTORY.SKU 
            FROM INVENTORY 
            JOIN TITLE ON INVENTORY.Title_ID = TITLE.Title_ID 
            WHERE INVENTORY.Condition = 'Used'""")
        results = cursor.fetchall()
        print("Title | SKU")
        for row in results:
            print(row)

    elif choice == "3":
        cursor.execute("SELECT Name, HourlyRate FROM EMPLOYEE WHERE HourlyRate >= 20.00")
        results = cursor.fetchall()
        print("Name | Hourly")
        for row in results:
            print(f"{row[0]} {row[1]:.2f}")

    elif choice == "4":
        print("Before:")
        print(" ID | Email")
        cursor.execute("SELECT Customer_ID, EmailAddress FROM MEMBER WHERE Customer_ID = 1")
        print(cursor.fetchone())
        
        cursor.execute("UPDATE MEMBER SET EmailAddress = 'johndoe@outlook.com' WHERE Customer_ID = 1")
        connection.commit()
        print("After:")
        print(" ID | Email")
        cursor.execute("SELECT Customer_ID, EmailAddress FROM MEMBER WHERE Customer_ID = 1")
        print(cursor.fetchone())
        
    elif choice == "5":
        print("Before:")
        print("SKU | Price")
        cursor.execute("SELECT SKU, Price FROM INVENTORY WHERE SKU = 'SKU-001'")
        print(cursor.fetchone())

        cursor.execute("UPDATE INVENTORY SET Price = 19.99 WHERE SKU = 'SKU-001'")
        connection.commit()

        print("After:")
        print("SKU | Price")
        cursor.execute("SELECT SKU, Price FROM INVENTORY WHERE SKU = 'SKU-001'")
        print(cursor.fetchone())
    

    elif choice == "6":
        cursor.execute("""SELECT EMPLOYEE.Name, SUM(Transactions.TotalCost) 
            FROM EMPLOYEE 
            JOIN TRANSACTIONS ON SSN = Employee_SSN 
            GROUP BY Name 
            ORDER BY SUM(TotalCost) ASC""")
        print("Name | Total Sales")
        for row in cursor.fetchall():
            print(row)

    elif choice == "7":
        print("Before:")
        print("Name | Hourly Rate")
        cursor.execute("SELECT Name, HourlyRate FROM EMPLOYEE WHERE Dept_ID = (SELECT Dept_ID FROM DEPARTMENT WHERE Dept_name = 'Inventory')")
        for row in cursor.fetchall(): print(f"{row[0]} {row[1]:.2f}")
        
        cursor.execute("UPDATE EMPLOYEE SET HourlyRate = HourlyRate * 1.10 WHERE Dept_ID = (SELECT Dept_ID FROM DEPARTMENT WHERE Dept_name = 'Inventory')")
        connection.commit()
        print("After:")
        print("Name | Hourly Rate")
        cursor.execute("SELECT Name, HourlyRate FROM EMPLOYEE WHERE Dept_ID = (SELECT Dept_ID FROM DEPARTMENT WHERE Dept_name = 'Inventory')")
        for row in cursor.fetchall(): print(f"{row[0]} {row[1]:.2f}")

    elif choice == "8":
        print("BEFORE:")
        print("Customer ID")
        cursor.execute("SELECT Customer_ID FROM MEMBER")
        print(cursor.fetchall())
        
        cursor.execute("DELETE FROM MEMBER WHERE Customer_ID = 5")
        connection.commit()
        
        print("AFTER:")
        print("Customer ID")
        cursor.execute("SELECT Customer_ID FROM MEMBER")
        print(cursor.fetchall())

    elif choice == "9":
        
        print("Before:")
        print("SSN | Name")
        cursor.execute("SELECT SSN, Name FROM EMPLOYEE")
        print(cursor.fetchall())
        
        cursor.execute("INSERT INTO EMPLOYEE (SSN, Name, DateOfBirth, StreetNumber, StreetName, City, State, Position, HourlyRate, PhoneNum, Dept_ID) VALUES ('999-00-1111', 'Sam Smith', '11-11-2005', '123', 'Beaver', 'Dearborn', 'MI', 'Sales',17.00, '111-222-3334', 1)")
        connection.commit()
        
        print("After:")
        print("SSN | Name")
        cursor.execute("SELECT SSN, Name FROM EMPLOYEE")
        print(cursor.fetchall())

    elif choice == "10":
        cursor.execute("""SELECT Title.Name, COUNT(CI.SKU) FROM TITLE 
            JOIN INVENTORY I ON Title.Title_ID = I.Title_ID 
            JOIN CHECKOUT_ITEMS CI ON I.SKU = CI.SKU 
            GROUP BY Title.Name ORDER BY 2 DESC""")
        print("New Employee:")
        for row in cursor.fetchall():
            print(row)

    elif choice == "0":
        break
    else:
        print("Invalid choice.")

connection.close()