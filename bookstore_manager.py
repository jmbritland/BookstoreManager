'''This Python program manages a database for a bookstore. It stores information about the books
in stock, including a unique ID number, title, author's name, and quantity in stock. Users may
add new books, edit information of books currently in the database, update the quantity in stock
of books currently in the database, delete books from the database, and search either by ID or
keywords in the title or author name. sqlite3 is used to communicate with the database.'''

import sqlite3

# ============================ Odds and ends for ease of use ==============================================

# For text styling
BOLD = "\033[1m"
ITALICS = "\033[3m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
PLAIN = "\033[0m"
# Info message for users, can be printed using info option in main menu
info_string = f'''\n\n\n{BOLD}Thank you for using the Bookstore Database Manager!{PLAIN}\n
This program is designed to store, retrieve, and change information about your bookstore's inventory.
Here are some tips to help you make the most of the program:
\n- Some of the text in this program is color coded.
    - {BLUE}Text in BLUE shows you commands you can use. Type these exactly as they are written without
     punctuation.
    - {GREEN}Text in GREEN tells you that you have successfully made changes in your database.
    - {RED}Text in RED tells you that there was an error. Often this means information was entered
     incorrectly.{PLAIN}
\n- The {BLUE}search{PLAIN} function will only find exact matches for your query. That means if the author's name 
    in the database is JJ Doe and you search for J. J. Doe, it will not turn up as a match. 
    - This means you should choose your keywords carefully and only include punctuation if it was entered
        that way originally. If you have trouble finding your book you can view a list of every book currently
        in your database by FIRST using the {BLUE}all{PLAIN} option and SECOND opening the file {ITALICS}current_books.txt{PLAIN},
        which is in the same folder as this program.
    - Also for this reason, it is best to format your authors' names consistently. The recommended format
        is to enter 'given-names last-name' without spaces or punctuation between initials, e.g. {GREEN}JJ Doe{PLAIN} 
        rather than {RED}J. J. Doe{PLAIN} or {RED}Doe, JJ{PLAIN}.
\n- Once an action has been taken, it cannot be undone! That's why the program always asks you to confirm
    whether you want to proceed before saving anything. Enter 'yes' with caution! If you enter 'no', no 
    changes will be saved that you've entered since the last time you were at the main menu. You can also
    enter 'cancel' at any time to return to the main menu.
\nWe hope these tips help you to use this program successfully.
\n{ITALICS}Technical information: 
This program is written in Python using the sqlite3 module for database management.{PLAIN}
'''

# ======================= Set-up database =============================================================

# Create books database with table
db = sqlite3.connect("ebookstore_db")
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS books(id CHAR(7) PRIMARY KEY, title TEXT,
                 author_name TEXT, qty INTEGER)''')
db.commit()

# Initialize with sample inventory; this portion of code would need to be deleted if user
# wanted to delete any of these records from the database as it currently attempts to add
# these records every time the code is run
sample_books = [("3001", "A Tale of Two Cities", "Charles Dickens", 30),
                ("3002", "Harry Potter and the Philosopher's Stone", "JK Rowling", 40),
                ("3003", "The Lion, the Witch, and the Wardrobe", "CS Lewis", 25),
                ("3004", "The Lord of the Rings", "JRR Tolkien", 37),
                ("3005", "Alice in Wonderland", "Lewis Carroll", 12)]
for book in sample_books:
    try:
        cursor.execute('''INSERT INTO books(id, title, author_name, qty)
                        VALUES(?,?,?,?)''', book)
    except:
        db.rollback()
    finally:
        db.commit()



# ======================= Define functions ===========================
def book_string(info_list):
    '''Prints a string with a book's information'''
    my_string = f"{info_list[1]} by {info_list[2]} (ID#{info_list[0]}); qty: {info_list[3]}"
    return my_string

def get_book_info():
    '''Requests book information from user and checks validity of inputs, then prints information
    given and asks for confirmation from user to save data. If user cancels, returns None. Else, 
    returns the book information in format [id, title, author_name, qty] for addition to database.'''
    print("\nGetting new book information.")
    while True:
        book_id = input("\nPlease enter book ID#: ").strip()
        if book_id.lower() == "cancel":
            return None
        try:
            if len(book_id) > 7:
                raise ValueError
            book_id = int(book_id)
            if book_id < 0:
                raise ValueError
            break
        except:
            print(f"{RED}Invalid input, try again.{PLAIN}")
    book_title = input("\nPlease enter the book's title: ").strip()
    if book_title.lower() == "cancel":
        return None
    book_author = input("\nPlease enter the name of the book's author (e.g. JJ Doe): ").strip()
    if book_author.lower() == "cancel":
        return None
    while True:
        book_qty = input("\nPlease enter the quantity of the book: ").strip()
        if book_qty.lower() == "cancel":
            return None
        try:
            book_qty = int(book_qty)
            if book_qty < 0:
                raise ValueError
            break
        except:
            print(f"{RED}Invalid input, try again.{PLAIN}")
    while True:
        confirmation = input(f'''\nWould you like to save the following information?{ITALICS}
{book_string([book_id, book_title, book_author, book_qty])}{PLAIN}
Yes or no: ''').lower().strip()
        if confirmation == "yes":
            return [book_id, book_title, book_author, book_qty]
        elif confirmation == "no" or confirmation == "cancel":
            return None
        else:
            print(f"{RED}Invalid input, try again.{PLAIN}")

def add_book():
    '''Uses get_book_info function to get data for a new book. Returns None if user cancels,
    otherwise adds the information in a new row in the books table.'''
    print('''\nAdding new book. Please note that the book will not be added if a duplicate
    ID# is found in the database.''')
    book_info = get_book_info()
    if book_info == None:
        print("\nReturning you to the main menu.")
        return None
    try:
        cursor.execute('''INSERT INTO books(id, title, author_name, qty)
        VALUES(?,?,?,?)''', tuple(book_info))
        print(f"{GREEN}\nSuccess! Book added to database.{PLAIN}")
    except Exception as error:
        if "UNIQUE constraint failed" in str(error):
            print(f"{RED}Duplicate ID# entered; cannot save information.{PLAIN}")
        db.rollback()
    finally:
        db.commit()

def search_id():
    '''Requests an ID from a user and searches for it in the ID column in the book database.
    Prints the book and returns its ID, or returns None if no matches found'''
    id_string = input("\nPlease enter the book's ID#: ").strip().lower()
    if id_string == "cancel":
        print("\nReturning you to the main menu")
        return None
    else:
        try:
            cursor.execute('''SELECT * FROM books WHERE id=?''', (id_string,))
            book = cursor.fetchone()
            print(f"{GREEN}Book found!{PLAIN}\n" + ITALICS + book_string(book) + PLAIN)
            return id_string
        except:
            print(f"{RED}Book not found, taking you back to the menu{PLAIN}")
            return None

def search_title():
    '''Requests a string from a user and searches for it in the title column of the book database.
    Prints a list of matching books, or returns None if no matches found.'''
    print("\nSearching by title")
    search_string = input("Please enter the keywords to search: ").strip().lower()
    if search_string.lower() == "cancel":
        print("\nReturning you to the main menu")
        return None
    cursor.execute('''SELECT * FROM books WHERE title LIKE ?''', ((f"%{search_string}%"),))
    books = cursor.fetchall()
    print()
    if len(books) == 0:
        print(f"{RED}\nNo books found matching your search. Returning you to the main menu. {PLAIN}")
        return None
    print(f"{GREEN}Books matching your query:{PLAIN}")
    for book in books:
        print(ITALICS + book_string(book) + PLAIN)
    print(PLAIN)

def search_author():
    '''Requests a string from a user and searches for it in the author_name column of the
    book database. Prints a list of matching books, or returns None if no matches found.'''
    print("\nSearching by author")
    search_string = input("Please enter the author's name: ").strip()
    if search_string.lower() == "cancel":
        print("\nReturning you to the main menu")
        return None
    cursor.execute('''SELECT * FROM books WHERE author_name LIKE ?''', ((f"%{search_string}%"),))
    books = cursor.fetchall()
    print()
    if len(books) == 0:
        print(f"{RED}\nNo books found matching your search. Returning you to the main menu{PLAIN}")
        return None
    print(f"{GREEN}Books matching your query:{PLAIN}")
    for book in books:
        print(ITALICS + book_string(book) + PLAIN)
    print(PLAIN)

def edit_book():
    '''Uses the search_id function to search for a book, then uses the get_book_info
    function to get the updated information of the book. Returns None if user cancels,
    otherwise updates information in database.'''
    print('''\nPlease enter the ID# of the book you want to edit. If you don't know the book's 
ID#, you may wish to use the search function first to find it.''')
    book_id = search_id()
    if book_id == None:
        return None
    book_info = get_book_info()
    if book_info == None:
        print("\nReturning you to the main menu.")
        return None
    book_info.append(book_id)
    try:
        cursor.execute('''UPDATE books
                        SET id=?, title=?, author_name=?, qty=?
                        WHERE id=?''', tuple(book_info))
        print(f"{GREEN}\nSuccess! Book data edited in database.{PLAIN}")
    except:
        db.rollback()
        print(f"{RED}There was an error saving the information.{PLAIN}")
    finally:
        db.commit()

def update_qty():
    '''Uses the search_id function to search for a book, then requests a new quantity 
    and checks for validity. Returns None if user cancels, otherwise updates information 
    in database.'''
    print('''Please enter the ID# of the book you want to update. If you don't know the book's
ID#, you may wish to use the search function first to find it.''')
    book_id = search_id()
    if book_id == None:
        return None
    while True:
        new_quantity = input("\nPlease enter the new quantity: ").strip()
        if new_quantity.lower() == "cancel":
            return None
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                raise ValueError
            break
        except:
            print(f"{RED}Invalid input, please try again.{PLAIN}")
    while True:
        confirmation = input(f'''\nWould you like to update the quantity of ID#{book_id} to {new_quantity}?
        Type 'yes' or 'no': ''').strip()
        if confirmation.lower() == "no" or confirmation.lower() == "cancel":
            print("\nReturning you to the main menu.")
            return None
        elif confirmation.lower() == "yes":
            break
        else:
            print(f"{RED}Invalid input, please try again.{PLAIN}")
    cursor.execute('''UPDATE books SET qty=? WHERE id=?''', (new_quantity,book_id))
    print(f"\n{GREEN}\nSuccess! Book quantity updated in database.{PLAIN}")
        
def delete_book():
    '''Uses the search_id function to search for a book, then asks for confirmation. 
    Returns None if user cancels, otherwise deletes record in database'''
    print('''\nDeleting a book.
\nPlease enter the ID# of the book you want to delete. If you don't know the book's
ID#, you may wish to use the search function first to find it.''')
    book_id = search_id()
    if book_id == None:
        return None
    while True:
        confirmation = input(f'''\nAre you sure you want to delete ID#{book_id}?
Enter yes or no: ''').strip().lower()
        if confirmation == "no" or confirmation == "cancel":
            print("\nReturning you to the main menu.")
            return None
        elif confirmation == "yes":
            break
    try:
        cursor.execute('''DELETE FROM books WHERE id=?''', (book_id,))
        print(f"{GREEN}\nSuccess, ID#{book_id} deleted!{PLAIN}")
    except Exception as error:
        print(error)

def print_all():
    '''Prints the book_string of each book in the database to an external txt file for
    the user to view all books currently in the database.'''
    print("\n" + 92 * "-")
    print("Updating current_books.txt; you may read this file to see what is currently in the database")
    print(92 * "-")
    cursor.execute('''SELECT * FROM books''')
    books = cursor.fetchall()
    books_file = open("current_books.txt", "w")
    for book in books:
        books_file.write(book_string(book) + "\n")
    books_file.close()



# =========================== Main menu loop ========================================================

print("\n" + 30 * "-" + f"{BOLD}\nWelcome to the Bookstore Database Manager!{PLAIN}\n" + "-" * 30)

while True:
    user_option = input(f'''\n***
{BOLD}Main menu - Please select an option:{PLAIN}\n
{BLUE}add{PLAIN} - Add a book to the database
{BLUE}edit{PLAIN} - Edit a book's information in the database
{BLUE}update{PLAIN} - Update a book's quantity
{BLUE}delete{PLAIN} - Remove a book from the database
{BLUE}search{PLAIN} - Search the books in the database
{BLUE}all{PLAIN} - Update current_books.txt with a list of all books currently in the database
{BLUE}info{PLAIN} - Read info about the program, including tips to make the most of it
{BLUE}exit{PLAIN} - Exit the program
(You may enter {BLUE}cancel{PLAIN} at anytime to return to this menu)\n
Enter option here: ''').strip().lower()

    if user_option == "add":
        add_book()

    elif user_option == "edit":
        edit_book()

    elif user_option == "update":
        update_qty()

    elif user_option == "delete":
        delete_book()

    elif user_option == "search":
        while True:
            user_option = input(f"\nEnter '{BLUE}id{PLAIN}', '{BLUE}title{PLAIN}', or '{BLUE}author{PLAIN}' to select search field: ").lower().strip()
            if user_option == "cancel":
                break
            elif user_option == "id":
                search_id()
                break
            elif user_option == "title":
                search_title()
                break
            elif user_option == "author":
                search_author()
                break
            else:
                print("Option not recognized, try again")

    elif user_option == "all":
        print_all()

    elif user_option == "info":
        print(info_string)

    elif user_option == "exit":
        print("\n" + 8 * "-")
        print(f"{BOLD}Goodbye!{PLAIN}")
        print(8 * "-" + "\n")
        break

    else:
        print(f"\n{RED}Option not recognized. Please try again.{PLAIN}")
