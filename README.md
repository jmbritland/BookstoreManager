#Thank you for viewing my Bookstore Manager project!

##What does it do?
This program was designed to maintain a database for a bookstore. It stores information about the books in stock, including a unique ID number, title, 
author's name, and quantity in stock. Users may add new books, edit information of books currently in the database, update the quantity in stock of books 
currently in the database, delete books from the database, and search either by ID or keywords in the title or author name.

##Why was this created?
I created this program as a part of my Software Engineering bootcamp with HyperionDev. This bootcamp was designed to prepare students for their first job 
in tech by teaching Python and a variety of other coding concepts, practices, and tools. This project showcases my learning about databases; the program 
is written in Python and uses SQL (by way of the sqlite3 module) to create and communicate with the database.

##How do I set up the program?
The primary program file, **bookstore_manager.py**, was built in Visual Studio Code and is ready to be run within the IDE (I have not tested it with other 
IDEs). If you wish to run it from a Windows command prompt, you must first run **install.bat** to ensure your system is configured for ANSII text styling 
escape codes. Then, you can run the program by opening **bookstore_manager.bat**.
**Important - The program includes 5 books as sample inventory, which were required by the task specifications. This section of the code should be deleted 
or commented out if you want to delete the sample records; currently, the program will attempt to add these records every time the program is run. The section 
that needs deleting is found in the "Set up database" section of the code and is marked with a comment noting that it should be deleted.**
For experimenting with the code, it is also recommended that you leave the sample records and include a 'DROP TABLE' SQL command at the end of the program so 
that the database resets at the end of each run.

##Overview of this program
On starting the run, users are greeted, then presented with this recurring menu:
![Image of the program's main menu](https://user-images.githubusercontent.com/120101780/213191988-063fc8fc-a728-4f10-9f21-f37841e4143b.png)
Users may enter 'cancel' to return to the main menu from within functions, and may enter 'exit' in the main menu to end the run.
####Add option
![Demo image of the 'add' option](https://user-images.githubusercontent.com/120101780/213193241-98950b3c-e8af-4f5d-9605-d4ebd560102c.png)
This option allows users to add a new record to the database. It checks for validity when entering the ID# and the quantity and confirms that the user wants 
to proceed before altering the database. New records cannot be added if a duplicate ID# is entered.
####Edit option
![Demo image of the 'edit' option](https://user-images.githubusercontent.com/120101780/213194778-2b8f9b2f-47a8-40a3-9be2-1ef2070a93bc.png)
This option allows users to edit as many fields as desired within a record. The same validity checks are made as in the add option.
####Update option
![Demo image of the 'update' option](https://user-images.githubusercontent.com/120101780/213195194-928a3747-f19c-4134-a1b7-c0fd74f6ca78.png)
This option allows users to update the quantity field only with a validity check and confirmation before saving.
####Delete option
![Demo image of the 'delete' option](https://user-images.githubusercontent.com/120101780/213195888-b5b0ff1c-0081-4418-af3f-6d908365fb8d.png)
This option allows users to select a record to delete from the database.
####Search option
![Demo image of the 'search' option](https://user-images.githubusercontent.com/120101780/213196529-06ec5ecd-37cd-44fd-bb31-d2f67f23e01f.png)
This option allows users to search for a book. ID search will find an exact match; title and author search will look for any exact matches with the search
term within the respective column.
####All option
![Demo image of the 'all' option](https://user-images.githubusercontent.com/120101780/213197044-94ed68bb-5607-4f4f-b46e-9a39ed75b995.png)
This option creates or overwrites the file **current_books.txt** with a list of all books currently in the database. The list does not update every 
time a change is made to the database; it only updates when the 'all' option is used.
####Info option
In addition, there is an 'info' option that prints some information about the program, including a few tips for best use.
