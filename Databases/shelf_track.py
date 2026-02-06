"""
Bookstore Management System (shelf_track.py)

This program manages an ebookstore inventory with books and authors.
Features:
- Add, update, delete, search books
- View all books with author details
- Robust input validation, error handling
- SQLite database persistence

Author: Nyandano Mathoma
"""

import sqlite3


# -------------------------------
# Database Setup
# -------------------------------

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect("ebookstore.db")


def create_tables():
    """Create book and author tables if they don't exist."""
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS author (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authorID INTEGER,
            qty INTEGER,
            FOREIGN KEY (authorID) REFERENCES author(id)
        )
        """)

        conn.commit()


def populate_initial_data():
    """Insert initial sample data if tables are empty."""
    with connect_db() as conn:
        cursor = conn.cursor()

        # Insert authors
        authors = [
            (1290, "Charles Dickens", "England"),
            (8937, "J.K. Rowling", "England"),
            (2356, "C.S. Lewis", "Ireland"),
            (6380, "J.R.R. Tolkien", "South Africa"),
            (5620, "Lewis Carroll", "England"),
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO author (id, name, country)
            VALUES (?, ?, ?)
        """, authors)

        # Insert books
        books = [
            (3001, "A Tale of Two Cities", 1290, 30),
            (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
            (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
            (3004, "The Lord of the Rings", 6380, 37),
            (3005, "Alice’s Adventures in Wonderland", 5620, 12),
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        """, books)

        conn.commit()


# -------------------------------
# Validation Helpers
# -------------------------------

def validate_id(id_value):
    """Validate that ID is a 4-digit integer."""
    return str(id_value).isdigit() and len(str(id_value)) == 4


def validate_qty(qty_value):
    """Validate that quantity is a non-negative integer."""
    return str(qty_value).isdigit() and int(qty_value) >= 0


# -------------------------------
# CRUD Operations
# -------------------------------

def add_book():
    """Add a new book to the database with validation."""
    try:
        book_id = input("Enter book ID (4 digits): ")
        if not validate_id(book_id):
            print("Invalid ID. Must be a 4-digit number.")
            return

        title = input("Enter book title: ").strip()

        author_id = input("Enter author ID (4 digits): ")
        if not validate_id(author_id):
            print("Invalid Author ID. Must be a 4-digit number.")
            return

        qty = input("Enter quantity: ")
        if not validate_qty(qty):
            print("Invalid quantity. Must be a non-negative number.")
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO book (id, title, authorID, qty)
                VALUES (?, ?, ?, ?)
            """, (int(book_id), title, int(author_id), int(qty)))
            conn.commit()
            print("Book added successfully!")

    except sqlite3.IntegrityError:
        print("Error: Book ID already exists.")
    except Exception as error:
        print(f"An error occurred: {error}")


def update_book():
    """Update book information (quantity, title, or author)."""
    book_id = input("Enter the book ID to update: ")
    if not validate_id(book_id):
        print("Invalid ID. Must be a 4-digit number.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT book.title, author.name, author.country, book.qty
            FROM book
            INNER JOIN author ON book.authorID = author.id
            WHERE book.id = ?
        """, (book_id,))
        record = cursor.fetchone()

        if not record:
            print("Book not found.")
            return

        print("\nCurrent details:")
        print(f"Title: {record[0]}")
        print(f"Author: {record[1]}")
        print(f"Country: {record[2]}")
        print(f"Qty: {record[3]}")

        print("\nWhat do you want to update?")
        print("1. Quantity\n2. Title\n3. AuthorID\n4. Author details")
        choice = input("Enter choice: ")

        if choice == "1":
            qty = input("Enter new quantity: ")
            if not validate_qty(qty):
                print("Invalid quantity.")
                return
            cursor.execute("UPDATE book SET qty = ? WHERE id = ?",
                           (int(qty), int(book_id)))

        elif choice == "2":
            new_title = input("Enter new title: ").strip()
            cursor.execute("UPDATE book SET title = ? WHERE id = ?",
                           (new_title, int(book_id)))

        elif choice == "3":
            new_author_id = input("Enter new Author ID (4 digits): ")
            if not validate_id(new_author_id):
                print("Invalid Author ID.")
                return
            cursor.execute("UPDATE book SET authorID = ? WHERE id = ?",
                           (int(new_author_id), int(book_id)))

        elif choice == "4":
            new_name = input("Enter new Author name: ").strip()
            new_country = input("Enter new Author country: ").strip()
            cursor.execute("""
                UPDATE author SET name = ?, country = ?
                WHERE id = (SELECT authorID FROM book WHERE id = ?)
            """, (new_name, new_country, int(book_id)))

        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Update successful!")


def delete_book():
    """Delete a book by ID."""
    book_id = input("Enter the book ID to delete: ")
    if not validate_id(book_id):
        print("Invalid ID. Must be a 4-digit number.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM book WHERE id = ?", (int(book_id),))
        if cursor.rowcount == 0:
            print("Book not found.")
        else:
            conn.commit()
            print("Book deleted successfully!")


def search_books():
    """Search for a book by title or ID."""
    choice = input("Search by (1) ID or (2) Title? ")

    with connect_db() as conn:
        cursor = conn.cursor()

        if choice == "1":
            book_id = input("Enter book ID: ")
            cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
        elif choice == "2":
            title = input("Enter part of the title: ")
            cursor.execute("SELECT * FROM book WHERE title LIKE ?",
                           ('%' + title + '%',))
        else:
            print("Invalid choice.")
            return

        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No matching books found.")


def view_books():
    """View details of all books and their authors."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
        """)
        records = cursor.fetchall()

        if not records:
            print("No books available.")
            return

        for title, author, country in records:
            print("\n----------------------------------------")
            print(f"Title: {title}")
            print(f"Author's Name: {author}")
            print(f"Author's Country: {country}")
            print("----------------------------------------")


# -------------------------------
# Menu System
# -------------------------------

def main_menu():
    """Display menu and route to functions."""
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            view_books()
        elif choice == "0":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")


# -------------------------------
# Program Entry Point
# -------------------------------

if __name__ == "__main__":
    create_tables()
    populate_initial_data()
    main_menu()
