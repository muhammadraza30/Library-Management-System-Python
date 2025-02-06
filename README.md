# Library Management System

## Overview
This Library Management System is a Python-based application designed to manage books, authors, readers, and library operations efficiently. It provides functionalities for librarians to manage books and members, and for readers to borrow, return, or purchase books. The application supports multiple user roles, including Librarian, Reader, and Member.

## Features

### Librarian:
- Add new books to the library.
- View available books in the library.
- Search for books by title.
- Verify member details.
- Issue and return books for members.
- Calculate fines for late returns.
- Generate bills for members.

### Reader:
- Borrow books from the library.
- Return borrowed books.
- View borrowed books.
- Purchase books from the library.
- View purchased books.
- View books written by specific authors.

### Member Management:
- Add new members.
- View member details.
- Manage book issuance and returns for members.
- Process payments for member bills.

## Classes and Responsibilities

### `Person`
Base class for all people in the system (e.g., `Author`, `Reader`).
- **Attributes:** `name`
- **Methods:** `get_name()`, `whoyouare()`

### `Author`
Inherits from `Person`.
- **Attributes:** `books_written`
- **Methods:** `add_book(book)`, `show_books_written()`

### `Reader`
Inherits from `Person`.
- **Attributes:** `books`, `purchased_books`
- **Methods:** `borrow_book(book)`, `return_book(library, book, member)`, `show_books()`, `purchase_book(book, library)`, `show_purchased_books()`

### `Book`
Represents a book in the library.
- **Attributes:** `book_ID`, `author`, `name`, `price`, `status`, `edition`, `date_of_purchase`, `owner`
- **Methods:** `update_status(status)`, `change_owner(new_owner)`, `display()`

### `Library`
Manages the library's collection of books and readers.
- **Attributes:** `books`, `readers`, `authors`
- **Methods:** `new_book(book)`, `lend_book(book, reader)`, `take_back_book(book, reader)`, `show_books()`, `add_reader(reader)`, `get_reader(name)`

### `Librarian`
Handles library operations.
- **Attributes:** `name`, `password`
- **Methods:** `search_book(library, book_title)`, `verify_member(members, member_id)`, `find_book(library, book_id)`, `issue_book(library, book, member)`, `return_book(library, book, member)`, `calculate_fine(member, days_late, fine_per_day)`, `create_bill(member, fine)`, `show_books(library)`

### `MemberRecord`
Manages individual member details and actions.
- **Attributes:** `member_id`, `name`, `member_type`, `date_of_membership`, `max_book_limit`, `address`, `phone_number`, `books`
- **Methods:** `get_member()`, `inc_book_issued()`, `dec_book_issued()`, `pay_bill(amount)`

## How to Run
1. Install Python 3.x if not already installed.
2. Copy the code into a Python file, e.g., `library_management.py`.
3. Run the script using the command:
   ```bash
   python library_management.py
   ```
4. Follow the on-screen instructions to navigate through the menus.

## Example Use Cases
### Adding a New Book
1. Log in as a librarian.
2. Select the "Add Book" option.
3. Provide the required book details, such as ID, title, author, price, edition, and purchase date.
4. The book is added to the library's collection.

### Borrowing a Book
1. Log in as a reader.
2. Select the "Borrow Book" option.
3. Choose a book from the available list.
4. The book's status is updated to "borrowed," and it is added to the reader's borrowed books list.

### Returning a Book
1. Log in as a reader.
2. Select the "Return Book" option.
3. Choose the book to return.
4. The book's status is updated to "available," and it is removed from the reader's borrowed books list.

## Limitations
- The system does not support a database backend; all data is stored in memory during runtime.
- No concurrency control for simultaneous users.
- Minimal input validation; ensure correct inputs are provided.

## Future Enhancements
- Integrate with a database for persistent storage.
- Add a graphical user interface (GUI) for better usability.
- Implement user authentication and role-based access control.
- Add email notifications for due dates and fines.

## License
This project is open-source and available under the [MIT License](LICENSE).
