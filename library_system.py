import json

fname = 'books.json'
borrowed_file = 'borrowed.json'

# ---------------- LOAD BOOKS ----------------
try:
    with open(fname, 'r') as fhand:
        books = json.load(fhand)
except FileNotFoundError:
    books = []

if type(books) == dict:
    books = [books]

# ---------------- LOAD BORROWED ----------------
try:
    with open(borrowed_file, 'r') as fhand:
        borrowed = json.load(fhand)
except:
    borrowed = []


# ---------------- ADD BOOK  ----------------
def add_book():
    print("\n - - - - - Add a New Book - - - - - - ")
    authors = input("Enter Author Name:")                   
    title = input("Enter Title Name:")
    category = input("Enter Category:")

    print(" - - - - Data Structure: Dictionary - - - - - ")                         

    book = {
        "author" : authors,
        "title" : title,
        "category" : category,
        "available" : True
    }

    print("\nBook Dictionary Created")                      
    print(book)

    for item in book:
        print(item)

    print("Key value pair: ")
    for key, val in book.items():
        print(key, ":", val)

    print("\nBook added to the system")

    books.append(book)

    try:
        with open(fname,'w') as fhand:
            json.dump(books,fhand)
            print('books are serialised\n')
    except Exception as e:
        print("Error saving file:", e)


# ---------------- SEARCH BOOK ----------------
def search_book():
    while True:
        print("\n- - - - - - - Search For A Book - - - - - - -")

        search_term = input ("Enter a book title or author to search:")

        found = False

        for item in books:
            if search_term.lower() in item["title"].lower() or search_term.lower() in item["author"].lower():
                print("\nBook Found:")
                for key, val in item.items():
                    print(key, ":", val)
                found = True

        if not found:
            print("No matching book found. Try again.")
        else:
            break


# ---------------- VIEW BOOKS ----------------
def view_books():
    print("\n- - - - - - -  View All Books - - - - - - -")
    if not books:
        print("No books in the system yet")
    else:
        for item in books:
            print ("\nbooks:")
            for key, val in item.items():
                print(key, ":", val)


# ---------------- DELETE BOOK ----------------
def delete_book():
    title = input("Enter exact Title to delete: ")

    new_books = []
    removed = False

    for item in books:
        if item["title"].lower() == title.lower():
            removed = True
        else:
            new_books.append(item)

    if removed:
        try:
            with open(fname, 'w') as fhand:
                json.dump(new_books, fhand)
            books.clear()
            books.extend(new_books)
            print("Book deleted successfully.")
        except Exception as e:
            print("Error saving file:", e)
    else:
        print("No matching book found.")


# ---------------- BORROW BOOK ----------------
def borrow_book():
    user = input("Enter your name or email: ")
    title = input("Enter exact book title to borrow: ")

    for item in books:
        if item["title"].lower() == title.lower():
            if item["available"] == True:
                item["available"] = False
                borrowed.append({"user": user, "title": title})

                with open(fname, 'w') as fhand:
                    json.dump(books, fhand)

                with open(borrowed_file, 'w') as fhand:
                    json.dump(borrowed, fhand)

                print("Book borrowed successfully.")
            else:
                print("Book already borrowed.")
            return

    print("Book not found.")


# ---------------- RETURN BOOK ----------------
def return_book():
    user = input("Enter your name or email: ")
    title = input("Enter exact book title to return: ")

    found = False

    for record in borrowed:
        if record["user"] == user and record["title"].lower() == title.lower():
            borrowed.remove(record)
            found = True

            for item in books:
                if item["title"].lower() == title.lower():
                    item["available"] = True

            with open(fname, 'w') as fhand:
                json.dump(books, fhand)

            with open(borrowed_file, 'w') as fhand:
                json.dump(borrowed, fhand)

            print("Book returned successfully.")
            break

    if not found:
        print("No record of this borrowed book.")
