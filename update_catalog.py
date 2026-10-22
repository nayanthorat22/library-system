"""
Safe Catalog Updater Script
Updates existing book records, preserves user accounts, active loans, and borrowing history.
Adds 79 realistic Indian novels, popular English novels, and domain books.
Safe to run repeatedly (idempotent).
"""

from app import create_app
from app.models import db, Book, Loan
from app.books_data import BOOKS_COLLECTION

def update_book_catalog():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("STARTING SAFE BOOK CATALOG UPDATE")
        print("=" * 60)

        # 1. Map existing books by ISBN
        existing_books = Book.query.all()
        existing_by_isbn = {b.isbn: b for b in existing_books}
        new_isbns = {b_data["isbn"] for b_data in BOOKS_COLLECTION}

        print(f"Current books in database: {len(existing_books)}")
        print(f"Target books in new collection: {len(BOOKS_COLLECTION)}")

        added_count = 0
        updated_count = 0
        skipped_or_retained_count = 0

        # 2. Add or update books from BOOKS_COLLECTION
        for b_data in BOOKS_COLLECTION:
            isbn = b_data["isbn"]
            if isbn in existing_by_isbn:
                # Update existing book attributes while respecting active loan counts
                book = existing_by_isbn[isbn]
                borrowed_copies = book.total_copies - book.available_copies
                if borrowed_copies < 0:
                    borrowed_copies = 0

                # Ensure total_copies is at least borrowed_copies
                new_total = max(b_data["total_copies"], borrowed_copies)
                book.title = b_data["title"]
                book.author = b_data["author"]
                book.category = b_data["category"]
                book.publication_year = b_data["publication_year"]
                book.description = b_data.get("description")
                book.total_copies = new_total
                book.available_copies = new_total - borrowed_copies
                
                updated_count += 1
            else:
                # Create new book record
                new_book = Book(
                    title=b_data["title"],
                    author=b_data["author"],
                    isbn=b_data["isbn"],
                    category=b_data["category"],
                    publication_year=b_data["publication_year"],
                    total_copies=b_data["total_copies"],
                    available_copies=b_data["total_copies"],
                    description=b_data.get("description")
                )
                db.session.add(new_book)
                added_count += 1

        db.session.commit()
        print(f"Successfully added: {added_count} new books")
        print(f"Successfully updated: {updated_count} existing books")

        # 3. Clean up obsolete books NOT in the new collection, ONLY IF they have NO loans
        all_current_books = Book.query.all()
        removed_count = 0
        for b in all_current_books:
            if b.isbn not in new_isbns:
                # Check for any loan reference (active or historical)
                has_any_loans = Loan.query.filter_by(book_id=b.id).first() is not None
                if not has_any_loans:
                    db.session.delete(b)
                    removed_count += 1
                else:
                    print(f"Preserving historical book with loans: {b.title} (ID:{b.id})")
                    skipped_or_retained_count += 1

        db.session.commit()
        if removed_count > 0:
            print(f"Safely removed {removed_count} obsolete unreferenced books.")

        final_book_count = Book.query.count()
        print(f"Final total books in catalogue: {final_book_count}")
        print("=" * 60)
        print("CATALOG UPDATE FINISHED SUCCESSFULLY!")
        print("=" * 60)

if __name__ == '__main__':
    update_book_catalog()
