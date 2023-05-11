# Package imports for MySQL connector, datetime and tkinter
import mysql.connector
import datetime
from tkinter import *

# MySQL connection to database syntax
db = mysql.connector.connect(
    host="127.0.0.1",                   # can be taken from the tab opened by 'manage connections' in the database tab header.
    user="root",
    password="",                        # blank if no password is set.
#    database="pyinventoryproject"  # <--- Directly interacts with an existing database. Uncomment and enter the name
                                        #      of the database for fluid and smooth testing. Comment out the database creation block.
)

# Database creation, referencing and creation of table (Comment out if using the direct connection method above).
cursor = db.cursor()  # Assign object cursor to variable 'cursor'.
cursor.execute("CREATE DATABASE if not exists inventoryproject")
cursor.execute("USE inventoryproject")  # Sets the above database to default for the rest of the commands in MySQL.
cursor.execute(
    "CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, quantity INT NOT NULL, "
    "price DECIMAL(10, 2) NOT NULL, currency VARCHAR(3) NOT NULL DEFAULT 'MYR', expiry_date DATE)")  # Creates a table with certain types (Refer to report).
cursor.close()  # Must always close the cursor object after use.


# Function for adding items to the table (Defining their name, quantity, price and expiration date).
def add_item():
    cursor = db.cursor()
    item = input("Enter item name: ")
    # Statement for aborting the function can be seen commonly throughout the rest of the program.
    if item.lower() == 'abort':
        print("Operation aborted. Return to the GUI tab to start another task.")
        return
    # Get quantity, validate (Checks for positive numerical value) and stores it.
    while True:
        quantity = input("Enter quantity: ")
        if quantity.lower() == 'abort':                                        # abort code to stop process midway
            print("Operation aborted. Return to the GUI tab to start another task.")
            return
        try:
            quantity = float(quantity)                                         # Assigns data type float to the input if possible.
        except ValueError:
            print("Invalid input: Quantity should be a number.")               # Prints if alphabet or other characters present in input.
        else:
            if quantity <= 0:  # Checks for negative numbers
                print("Invalid input: Quantity should be a positive number.")  # Prints if input is negative.
            else:
                break                                                          # If valid input, breaks from loop and moves to next input.

    # Get price, validate (checks for negative & formats) and stores it
    price = input("Enter price (MYR): ")
    while True:
        try:
            if price.lower() == 'abort':                                   # abort code to stop process midway
                print("Operation aborted. Return to the GUI tab to start another task.")
                return
            price = float(price)                                           # assigns float data type to the price input variable if possible
            if price <= 0:                                                 # Checks for negative numbers
                raise ValueError                                           # Re-directs code to the ValueError to catch the error while keeping it in the loop
            else:
                price = round(price, 2)                                    # Returns a floating point number that is rounded to 2 decimal places of the input
            break                                                          # If valid input, breaks from loop and moves to next input.
        except ValueError:
            print("Invalid input: Price should be a positive number.")
            price = input("Enter price (MYR): ")

    # Get expiry date, validate (checks within realistic dates) and stores it
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
    while True:
        try:
            if expiry_date.lower() == 'abort':                             # abort code
                print("Operation aborted. Return to the GUI tab to start another task.")
                return
            year, month, day = map(int, expiry_date.split('-'))            # Code to assign an int data type to each variable and uses split function to separate the hyphens from data numbers
            date_obj = datetime.date(year, month, day)                     # Assign date object to date values
            if date_obj < datetime.date.today():                           # Mainly checks to see if year is the same and not in the past
                raise ValueError                                           # Re-directs code to the ValueError to catch the error while keeping it in the loop
            elif month == 2 and day > 28:                                  # Checks the date value and is aware to look out for february's inconsistency of having 28 days
                raise ValueError                                           # Re-directs code to the ValueError to catch the error while keeping it in the loop
            elif day > 31:                                                 # Was running into some errors and a was forced to use this line to define.
                raise ValueError                                           # Re-directs code to the ValueError to catch the error while keeping it in the loop
            break                                                          # If valid input, breaks from loop and moves to next input.
        except ValueError:                                                 # Catches the error, points the user's mistake out and prompts them to try again
            print("Invalid input. Expiry date should be a valid date in the future and in the format YYYY-MM-DD")
            expiry_date = input("Enter expiry date (YYYY-MM-DD): ")

    # Insert stored values into database
    sql = "INSERT INTO items (name, quantity, price, expiry_date) VALUES (%s, %s, %s, %s)"  # Template for inserting into MySQL with %s as placeholders for data
    values = (item, quantity, price, f"{year:04d}-{month:02d}-{day:02d}")                   # The stored user inputs to take place of placeholders and date formatted with f"
    cursor.execute(sql, values)                                                             # Execution code combining both variables of SQL command and inputs
    db.commit()                                                                             # Changes are committed and implemented to database
    print(cursor.rowcount, "record(s) inserted. Return to the GUI tab to start another task.")  # Print statement informs how many rows were affected and to go back to GUI
    cursor.close()                                                                             # Cursor closed at the end of the function


# Deletion function
def remove_item():
    cursor = db.cursor()
    # Get item name to remove
    id = input("Enter item id to remove (use the view button to view all id's): ")
    if id.lower() == 'abort':                                                               # abort code to stop process midway
        print("Operation aborted. Return to the GUI tab to start another task.")
        return
    sql = "DELETE FROM items WHERE id = %s"                                                 # Placeholder code to delete item
    values = (id,)                                                                          # cursor execute needs two parameters, so a single tuple is created to
                                                                                            # avoid creating a string using the comma
    cursor.execute(sql, values)                                                             # Execution code for combining variables like above
    db.commit()                                                                             # Changes are committed and implemented to database
    print(cursor.rowcount, "record(s) deleted. Return to the GUI tab to start another task.") # Print statement informs how many rows were affected and to go back to GUI
    cursor.close()                                                                           # Cursor closed at the end of the function


# Function that lists all the items in the table
def view_items():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM items")                               # Retrieve all items from database and print
    result = cursor.fetchall()                                          # Fetch all (remaining) rows of a query result, returning them as a list of tuples.
                                                                        # An empty list is returned if there is no more record to fetch.
    print("Search result(s):")
    for row in result:                                                  # For loop for printing search results in each corresponding row and GUI instructions to go back
        print("ID:", row[0])
        print("Name:", row[1])
        print("Quantity:", row[2])
        print("Price:", row[3])
        print("Currency:", row[4])
        print("Expiry Date:", row[5])
        print()
    print("Return to the GUI tab to start another task.")
    cursor.close()


# Function for updating a cell in the SQL table
def update_items():
    column_name = input("Which property of the item do you want to change? (Enter column name): ")
    if column_name.lower() == 'abort':                                 # abort code to stop process midway
        print("Operation aborted. Return to the GUI tab to start another task.")
        return

    values = input("Enter the change you want to make: ")
    while True:
        if values == 'abort':                                          # abort code to stop process midway
            print("Operation aborted. Return to the GUI tab to start another task.")
            return
        if column_name == 'quantity':
            try:
                values = float(values)                                 # assigns float data type to the input variable if possible
            except ValueError:                                         # Catches the error, points the user's mistake out and prompts them to try again
                print("Invalid input: Quantity should be a number.")
                values = input("Enter the change you want to make: ")
            else:
                if values <= 0:                                        # Checks for negative numbers
                    print("Invalid input: Quantity should be a positive number.")
                    values = input("Enter the change you want to make: ")
                else:
                    break                                              # If valid input, breaks from loop and moves to next input.

        if column_name == 'price':
            try:
                values = float(values)                                 # assigns float data type to the input variable if possible
                if values <= 0:                                        # Checks for negative numbers
                    raise ValueError                                   # Re-directs code to the ValueError to catch the error while keeping it in the loop
                else:
                    values = round(values, 2)                          # Returns a floating point number that is rounded to 2 decimal places of the input
                break                                                  # If valid input, breaks from loop and moves to next input.
            except ValueError:                                         # Catches the error, points the user's mistake out and prompts them to try again
                print("Invalid input: Price should be a positive number.")
                values = input("Enter the change you want to make: ")

        if column_name == 'name':                                      # Code to prevent the user from leaving a field blank (especially name) (experiment)
            if not values:
                print("Invalid input: Name cannot be empty.")
                values = input("Enter the change you want to make: ")
            else:
                break

        if column_name == 'expiry_date':
            try:
                if values == 'abort':                                  # abort code to stop process midway
                    print("Operation aborted. Return to the GUI tab to start another task.")
                    return
                expiry_date = datetime.datetime.strptime(values, '%Y-%m-%d')
                today = datetime.datetime.today()
                if expiry_date < today:                              # Makes sure that the item expires any day after current day (realism)
                    print("Invalid input: Expiry date should be a future date.")
                    values = input("Enter the change you want to make: ")
                else:
                    break                                            # If valid input, breaks from loop and moves to next input.
            except ValueError:                                       # Catches the error, points the user's mistake out and prompts them to try again
                print("Invalid input. Expiry date should be a valid date in the format YYYY-MM-DD.")
                values = input("Enter the change you want to make: ")

    row_id = input("Enter the id of the item you want to change: ") # Gets ID to check which item undergoes the change
    if row_id.lower() == 'abort':                                   # abort code to stop process midway
        print("Operation aborted. Return to the GUI tab to start another task.")
        return

    cursor = db.cursor()
    sql = "UPDATE items SET {} = %s WHERE id = %s".format(column_name)    # SQL code with placeholder variables and makeshift format code for column name
    cursor.execute(sql, (values, row_id))                                 # SQL code for execution
    db.commit()                                                           # SQL code for committing the change
    print(cursor.rowcount, "record(s) updated. Return to the GUI tab to start another task.")  # Code for verifying change
    cursor.close()


# Function for searching for specific data rows by using their names as a key
def search_items():
    cursor = db.cursor()
    name = input("Enter the exact item name to search: ")                 # Get exact item name to search
    if name.lower() == 'abort':                                           # abort code to stop process midway
        print("Operation aborted. Return to the GUI tab to start another task.")
        return
    sql = "SELECT * FROM items WHERE name = %s"                           # Search for item in database and print
    values = (name,)
    cursor.execute(sql, values)
    result = cursor.fetchall()
    if result:
        print("Search result(s):")
        for row in result:
            print("ID:", row[0])
            print("Name:", row[1])
            print("Quantity:", row[2])
            print("Price:", row[3])
            print("Currency:", row[4])
            print("Expiry Date:", row[5])
            print()
            print("Return to the GUI tab to start another task.")
    else:
        print("Item not found. Return to the GUI tab to start another task.")  # Code to run if item doesn't exist
    cursor.close()


# Function for terminating the program
def exit_program():
    db.close()                                   # Close database
    main.destroy()                               # Close tkinter window




# Basic GUI
main = Tk()
main.title("Inventory Program")

welcome_message = Label(main, text="Hi, welcome to the Perishable superstore inventory system!\nA database and table have "   # Welcome message
                                   "already been created in"
                                   "MySQL, check it out!\nYou can click on any of the buttons to get "
                                   "started\nYou can type abort during any of the operations to stop them.")
welcome_message.pack()

# Button adjustment and arrangement

# Functions for the color when hover feature
def on_enter(e):
    e.widget['background'] = 'cyan'
def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'


add_button = Button(main, text="Add Item", command=add_item, padx=20, pady=5, relief=RAISED, bd=5)
add_button.bind("<Enter>", on_enter)
add_button.bind("<Leave>", on_leave)
add_button.pack(pady=5)

remove_button = Button(main, text="Remove Item", command=remove_item, padx=20, pady=5, relief=RAISED, bd=5)
remove_button.bind("<Enter>", on_enter)
remove_button.bind("<Leave>", on_leave)
remove_button.pack(pady=5)

view_button = Button(main, text="View Items", command=view_items, padx=20, pady=5, relief=RAISED, bd=5)
view_button.bind("<Enter>", on_enter)
view_button.bind("<Leave>", on_leave)
view_button.pack(pady=5)

update_button = Button(main, text="Update Items", command=update_items, padx=20, pady=5, relief=RAISED, bd=5)
update_button.bind("<Enter>", on_enter)
update_button.bind("<Leave>", on_leave)
update_button.pack(pady=5)

search_button = Button(main, text="Search Items", command=search_items, padx=20, pady=5, relief=RAISED, bd=5)
search_button.bind("<Enter>", on_enter)
search_button.bind("<Leave>", on_leave)
search_button.pack(pady=5)

exit_button = Button(main, text="Exit Program", command=exit_program, padx=20, pady=5, relief=RAISED, bd=5)
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)
exit_button.pack(pady=5)


main.mainloop()
