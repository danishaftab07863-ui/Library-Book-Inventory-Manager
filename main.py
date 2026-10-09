import json
import os

class Book:
    """Class representing an individual book."""
    def __init__(self, book_id, title, author, is_issued=False):
        self.book_id = str(book_id)
        self.title = title
        self.author = author
        self.is_issued = is_issued

    def to_dict(self):
        """Convert Book object to dictionary for JSON storage."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "is_issued": self.is_issued
        }

    @staticmethod
    def from_dict(data):
        """Create a Book object from a dictionary."""
        return Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            is_issued=data.get("is_issued", False)
        )

    def __str__(self):
        status = "Issued" if self.is_issued else "Available"
        return f"[ID: {self.book_id}] {self.title} by {self.author} | Status: {status}"


class Library:
    """Class managing book inventory using HashMap/Dictionary for fast lookup."""
    def __init__(self, filename="books.json"):
        self.filename = filename
        # HashMap (dict): Key = book_id, Value = Book instance
        self.books = {}
        self.load_from_file()

    def add_book(self, book_id, title, author):
        """Add a new book to the library."""
        book_id = str(book_id)
        if book_id in self.books:
            print(f"❌ Error: Book with ID {book_id} already exists!")
            return False
        
        new_book = Book(book_id, title, author)
        self.books[book_id] = new_book
        self.save_to_file()
        print(f"✅ Book '{title}' added successfully!")
        return True

    def search_books(self, query):
        """Search books by title or author."""
        query_lower = query.lower()
        results = [
            book for book in self.books.values()
            if query_lower in book.title.lower() or query_lower in book.author.lower()
        ]
        return results

    def issue_book(self, book_id):
        """Issue a book by its ID."""
        book_id = str(book_id)
        if book_id not in self.books:
            print("❌ Error: Book ID not found.")
            return

        book = self.books[book_id]
        if book.is_issued:
            print(f"⚠️ Book '{book.title}' is already issued.")
        else:
            book.is_issued = True
            self.save_to_file()
            print(f"✅ Book '{book.title}' issued successfully!")

    def return_book(self, book_id):
        """Return an issued book by its ID."""
        book_id = str(book_id)
        if book_id not in self.books:
            print("❌ Error: Book ID not found.")
            return

        book = self.books[book_id]
        if not book.is_issued:
            print(f"⚠️ Book '{book.title}' was not issued.")
        else:
            book.is_issued = False
            self.save_to_file()
            print(f"✅ Book '{book.title}' returned successfully!")

    def generate_report(self):
        """Display summary statistics of the inventory."""
        total_books = len(self.books)
        issued_count = sum(1 for b in self.books.values() if b.is_issued)
        available_count = total_books - issued_count

        print("\n" + "=" * 30)
        print("      LIBRARY REPORT      ")
        print("=" * 30)
        print(f"Total Books      : {total_books}")
        print(f"Issued Books     : {issued_count}")
        print(f"Available Books  : {available_count}")
        print("=" * 30)

    def display_all_books(self):
        """List all books in inventory."""
        if not self.books:
            print("📭 Library is empty.")
            return
        
        print("\n--- Book List ---")
        for book in self.books.values():
            print(book)

    def save_to_file(self):
        """Save inventory dictionary to JSON file."""
        data = {book_id: book.to_dict() for book_id, book in self.books.items()}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """Load inventory from JSON file on startup."""
        if not os.path.exists(self.filename):
            self.books = {}
            return

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.books = {
                    book_id: Book.from_dict(book_data)
                    for book_id, book_data in data.items()
                }
        except (json.JSONDecodeError, Exception) as e:
            print(f"⚠️ Error loading data: {e}. Starting with empty library.")
            self.books = {}


def main():
    library = Library()

    while True:
        print("\n" + "="*35)
        print("  LIBRARY BOOK INVENTORY MANAGER  ")
        print("="*35)
        print("1. Add Book")
        print("2. Search Book (Title / Author)")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View All Books")
        print("6. Show Report")
        print("7. Exit")
        
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            book_id = input("Enter Book ID: ").strip()
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()
            if book_id and title and author:
                library.add_book(book_id, title, author)
            else:
                print("❌ All fields are required!")

        elif choice == "2":
            query = input("Enter Title or Author to search: ").strip()
            results = library.search_books(query)
            if results:
                print(f"\nFound {len(results)} matching book(s):")
                for book in results:
                    print(book)
            else:
                print("❌ No matching books found.")

        elif choice == "3":
            book_id = input("Enter Book ID to issue: ").strip()
            library.issue_book(book_id)

        elif choice == "4":
            book_id = input("Enter Book ID to return: ").strip()
            library.return_book(book_id)

        elif choice == "5":
            library.display_all_books()

        elif choice == "6":
            library.generate_report()

        elif choice == "7":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()