import sqlite3

# ---------- Database Setup ----------
def connect_db():
    return sqlite3.connect('ebookstore.db')

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER,
                qty INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            )
        ''')
        conn.commit()

# ---------- Data Population ----------
def populate_initial_data():
    books = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)
    ]
    authors = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")
    ]
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO book VALUES (?, ?, ?, ?)", books)
        cursor.executemany("INSERT OR IGNORE INTO author VALUES (?, ?, ?)", authors)
        conn.commit()

# ---------- Core Functions ----------
def add_book():
    try:
        book_id = int(input("Enter book ID (4-digit): "))
        title = input("Enter book title: ")
        author_id = int(input("Enter author ID (4-digit): "))
        qty = int(input("Enter quantity: "))
        with connect_db() as conn:
            conn.execute("INSERT INTO book VALUES (?, ?, ?, ?)", (book_id, title, author_id, qty))
            print("Book added successfully.")
    except Exception as e:
        print(f"Error: {e}")

def update_book():
    try:
        book_id = int(input("Enter book ID to update: "))
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, authorID, qty FROM book WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if not book:
                print("Book not found.")
                return
            print(f"Current title: {book[0]}, Author ID: {book[1]}, Quantity: {book[2]}")
            print("1. Update quantity\n2. Update title\n3. Update author info")
            choice = input("Choose an option: ")
            if choice == '1':
                new_qty = int(input("Enter new quantity: "))
                cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, book_id))
            elif choice == '2':
                new_title = input("Enter new title: ")
                cursor.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, book_id))
            elif choice == '3':
                author_id = book[1]
                cursor.execute("SELECT name, country FROM author WHERE id = ?", (author_id,))
                author = cursor.fetchone()
                print(f"Current author: {author[0]}, Country: {author[1]}")
                new_name = input("Enter new author name: ")
                new_country = input("Enter new author country: ")
                cursor.execute("UPDATE author SET name = ?, country = ? WHERE id = ?", (new_name, new_country, author_id))
            conn.commit()
            print("Update successful.")
    except Exception as e:
        print(f"Error: {e}")

def delete_book():
    try:
        book_id = int(input("Enter book ID to delete: "))
        with connect_db() as conn:
            conn.execute("DELETE FROM book WHERE id = ?", (book_id,))
            print("Book deleted.")
    except Exception as e:
        print(f"Error: {e}")

def search_books():
    title = input("Enter book title to search: ")
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + title + '%',))
        results = cursor.fetchall()
        if results:
            for book in results:
                print(f"ID: {book[0]}, Title: {book[1]}, Author ID: {book[2]}, Quantity: {book[3]}")
        else:
            print("No books found.")

def view_all_books():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author ON book.authorID = author.id
        ''')
        for title, name, country in cursor.fetchall():
            print(f"\nTitle: {title}\nAuthor's Name: {name}\nAuthor's Country: {country}")

# ---------- Main Menu ----------
def main():
    create_tables()
    populate_initial_data()
    while True:
        print("\n1. Enter book\n2. Update book\n3. Delete book\n4. Search books\n5. View details of all books\n0. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            view_all_books()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()