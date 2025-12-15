from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

BOOKS_FILE = "books.json"
BORROWED_FILE = "borrowed.json"

# ------------ LOAD OR CREATE JSON FILES ----------
def load_json(fname):
    if not os.path.exists(fname):
        return []
    with open(fname, "r") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
        except:
            return []

def save_json(fname, data):
    with open(fname, "w") as f:
        json.dump(data, f, indent=4)

books = load_json(BOOKS_FILE)
borrowed = load_json(BORROWED_FILE)


# ------------ HOME PAGE ----------
@app.route("/")
def home():
    return render_template("index.html")


# ------------ VIEW BOOKS ----------
@app.route("/view")
def view_books():
    return render_template("view.html", books=books)


# ------------ ADD BOOK ----------
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        category = request.form["category"]

        book = {
            "author": author,
            "title": title,
            "category": category,
            "available": True
        }

        books.append(book)
        save_json(BOOKS_FILE, books)

        return redirect("/view")

    return render_template("add.html")


# ------------ SEARCH BOOK ----------
@app.route("/search", methods=["GET", "POST"])
def search_book():
    results = []
    if request.method == "POST":
        term = request.form["term"].lower()

        for item in books:
            if term in item["title"].lower() or term in item["author"].lower():
                results.append(item)

    return render_template("search.html", results=results)


# ------------ DELETE BOOK ----------
@app.route("/delete", methods=["GET", "POST"])
def delete_book():
    if request.method == "POST":
        title = request.form["title"].lower()

        global books
        new_list = [b for b in books if b["title"].lower() != title]

        if len(new_list) != len(books):
            books = new_list
            save_json(BOOKS_FILE, books)
            message = "Book deleted successfully."
        else:
            message = "Book not found."

        return render_template("delete.html", message=message)

    return render_template("delete.html", message=None)


# ------------ BORROW BOOK ----------
@app.route("/borrow", methods=["GET", "POST"])
def borrow_book():
    if request.method == "POST":
        user = request.form["user"]
        title = request.form["title"].lower()

        for item in books:
            if item["title"].lower() == title:
                if item["available"]:
                    item["available"] = False

                    borrowed.append({"user": user, "title": item["title"]})
                    save_json(BOOKS_FILE, books)
                    save_json(BORROWED_FILE, borrowed)

                    return render_template("borrow.html", message="Book borrowed successfully.")
                else:
                    return render_template("borrow.html", message="Book already borrowed.")

        return render_template("borrow.html", message="Book not found.")

    return render_template("borrow.html", message=None)


# ------------ RETURN BOOK ----------
@app.route("/return", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        user = request.form["user"]
        title = request.form["title"].lower()

        for record in borrowed:
            if record["user"] == user and record["title"].lower() == title:
                borrowed.remove(record)

                for item in books:
                    if item["title"].lower() == title:
                        item["available"] = True

                save_json(BOOKS_FILE, books)
                save_json(BORROWED_FILE, borrowed)

                return render_template("return.html", message="Book returned successfully.")

        return render_template("return.html", message="No record found.")

    return render_template("return.html", message=None)


if __name__ == "__main__":
    app.run(debug=True)
