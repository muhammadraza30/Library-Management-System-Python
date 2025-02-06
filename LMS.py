class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def whoyouare(self):
        return "I am a ",self.name


class Author(Person):
    def __init__(self, name, books_written):
        super().__init__(name)
        self.books_written = books_written

    def add_book(self, book):
        self.books_written.append(book)

    def show_books_written(self):
        if not self.books_written:
            print(f"{self.name} has not written any books.")
        else:
            print(f"{self.name}'s written books:")
            for book in self.books_written:
                print(f"- {book.name}")


class Reader(Person):
    def __init__(self, name):
        super().__init__(name)
        self.books = []
        self.purchased_books = []

    def borrow_book(self, book):
        if book.status == "available":
            self.books.append(book)
            book.update_status("borrowed")
            book.change_owner(self.name)
            print(f"{self.name} borrowed the book: {book.name}")
        else:
            print(f"Book '{book.name}' is not available for borrowing.")

    def return_book(self, library, book, member):
        reader = library.get_reader(member.name)
        if reader and book in reader.books:
            library.take_back_book(book, reader)
            member.dec_book_issued()
            print(f"{member.name} has returned the book: {book.name}")
        else:
            print(f"{member.name} has not borrowed the book: {book.name}")

    def show_books(self):
        if not self.books:
            print(f"{self.name} has not borrowed any books.")
        else:
            print(f"{self.name}'s borrowed books:")
            print('_'*120)
            print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s"%("Book ID","Title","Author","Price","Status","Edition","Date of Purchase","Owner"))
            print('_'*120)
            for book in self.books:
                book.display()

    def purchase_book(self, book, library):
        if book.status == "available":
            self.purchased_books.append(book)
            book.update_status("purchased")
            book.change_owner(self.name)
            library.books.remove(book)
            print(f"{self.name} purchased the book: {book.name}")
        else:
            print(f"Book '{book.name}' is not available for purchase.")

    def show_purchased_books(self):
        if not self.purchased_books:
            print(f"{self.name} has not purchased any books.")
        else:
            print(f"{self.name}'s purchased books:")
            print('_'*120)
            print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s"%("Book ID","Title","Author","Price","Status","Edition","Date of Purchase","Owner"))
            print('_'*120)
            for book in self.purchased_books:
                book.display()

class Book:
    def __init__(self, book_ID, author, name, price, status, edition, date_of_purchase):
        self.book_ID = book_ID
        self.author = author
        self.name = name
        self.price = price
        self.status = status
        self.edition = edition
        self.date_of_purchase = date_of_purchase
        self.owner = "Library"  

    def update_status(self, status):
        self.status = status

    def change_owner(self, new_owner):
        self.owner = new_owner

    def display(self):
        print(f"{self.book_ID:<11}{self.name:<16}{self.author:<16}{self.price:<16}{self.status:<16}{self.edition:<16}{self.date_of_purchase:<21}{self.owner:<16}")


class Library:
    def __init__(self):
        self.books = []
        self.readers = []
        self.authors = {} 

    def new_book(self, book):
        if not any(b.book_ID == book.book_ID for b in self.books):
            self.books.append(book)
            print(f"New book '{book.name}' added to the library.")
            if book.author not in self.authors:
                self.authors[book.author] = Author(book.author, [])
            self.authors[book.author].add_book(book)
        else:
            print(f"Book with ID {book.book_ID} already exists.")      
            
    def lend_book(self, book, reader):
        reader.borrow_book(book)

    def take_back_book(self, book, reader):
        reader.return_book(book)

    def show_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            for book in self.books:
                book.display()

    def get_books(self):
        return self.books

    def add_reader(self, reader):
        if reader.name not in [r.get_name() for r in self.readers]:
            self.readers.append(reader)
        else:
            print(f"Reader with name {reader.name} already exists.")
    
    def get_reader(self, name):
        for reader in self.readers:
            if reader.get_name() == name:
                return reader
        print(f"No reader found with the name: {name}")
        return None

class Librarian:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def search_book(self, library, book_title):
        for book in library.get_books():
            if book.name.lower() == book_title.lower():
                return book
        return None

    def verify_member(self, members, member_id):
        return members.get(member_id)
    
    def find_book(self, library, book_id):
        for book in library.get_books():
            if book.book_ID == book_id:
                return book
        return None
        
    def issue_book(self, library, book, member):
        reader = library.get_reader(member.name)  
        if reader and member.number_of_books_issued < member.max_book_limit:
            library.lend_book(book, reader) 
            member.inc_book_issued()  
        else:
            print(f"{member.name} has reached the maximum book limit or reader not found!")

    def return_book(self, library, book, member):
        library.take_back_book(book, member)
        member.dec_book_issued()

    def calculate_fine(self, member, days_late, fine_per_day=10):
        return days_late * fine_per_day

    def create_bill(self, member, fine=0):
        total_amount_due = sum(book.price for book in member.books) + fine
        return total_amount_due

    def show_books(self, library):
        library.show_books()


class MemberRecord:
    def __init__(self, member_id, name, member_type, date_of_membership, max_book_limit, address, phone_number):
        self.member_id = member_id
        self.name = name
        self.member_type = member_type
        self.date_of_membership = date_of_membership
        self.number_of_books_issued = 0
        self.max_book_limit = max_book_limit
        self.address = address
        self.phone_number = phone_number
        self.books = []

    def get_member(self):
        return "ID: {}\nName: {}\nMember Type: {}\nDate of Membership: {}\nNumber of Books Issued: {}\nMax Book Limit: {}\nAddress: {}\nPhone Number: {}".format(
            self.member_id, 
            self.name, 
            self.member_type, 
            self.date_of_membership, 
            self.number_of_books_issued, 
            self.max_book_limit, 
            self.address, 
            self.phone_number)
        
    def inc_book_issued(self):
        if self.number_of_books_issued < self.max_book_limit:
            self.number_of_books_issued += 1
        else:
            print(f"{self.name} has reached the maximum book limit.")

    def dec_book_issued(self):
        if self.number_of_books_issued > 0:
            self.number_of_books_issued -= 1
        else:
            print(f"{self.name} has no books to return.")

    def pay_bill(self, amount):
        total_amount_due = sum(book.price for book in self.books)
        if amount >= total_amount_due:
            print(f"Payment successful! Total amount of {total_amount_due} paid by {self.name}.")
            self.books.clear()
            self.number_of_books_issued = 0
        else:
            print(f"Insufficient payment. You need to pay at least {total_amount_due}.")



def main():
    library = Library()
    librarian = Librarian("Raza", "1234")
    members = {} 

    while True:
        print("\n1. Librarian\n2. Reader\n3. Manage Members\n4. Exit")
        select = int(input("Enter your choice: "))

        if select == 1:
            username = input("Enter username: ")
            password = input("Enter Password: ")

            if username == librarian.name and password == librarian.password:
                while True:
                    print("\nLibrarian Menu:\n1. Add Book\n2. Show Library Books\n3. Search Book\n4. Verify Member\n5. Issue Book\n6. Return Book\n7. Calculate Fine\n8. Logout")
                    choice = int(input("Enter your choice: "))

                    if choice == 1:
                        book_id = int(input("Enter Book ID: "))
                        if any(book.book_ID == book_id for book in library.get_books()):
                            print(f"Book with ID {book_id} already exists. Please enter a unique ID.")
                            continue
                        title = input("Enter Book Title: ")
                        author_name = input("Enter Author Name: ")
                        price = float(input("Enter Book Price: "))
                        edition = input("Enter Book Edition: ")
                        date_of_purchase = input("Enter Date of Purchase: ")

                        author = Author(author_name, [])
                        book = Book(book_id, author_name, title, price, "available", edition, date_of_purchase)
                        author.add_book(book)
                        library.new_book(book)

                    elif choice == 2:
                        print('_' * 120)
                        print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s" % ("Book ID", "Title", "Author", "Price", "Status", "Edition", "Date of Purchase", "Owner"))
                        print('_' * 120)
                        librarian.show_books(library)

                    elif choice == 3:
                        book_title = input("Enter Book Title to search: ")
                        book = librarian.search_book(library, book_title)
                        print('_' * 120)
                        print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s" % ("Book ID", "Title", "Author", "Price", "Status", "Edition", "Date of Purchase", "Owner"))
                        print('_' * 120)
                        if book:
                            book.display()
                        else:
                            print("Book not found.")
                    elif choice == 4:
                        member_id = input("Enter Member ID to verify: ")
                        member = librarian.verify_member(members, member_id)
                        if member:
                            print("Member found:", member.get_member())
                        else:
                            print("Member not found.")

                    elif choice == 5:
                        member_id = input("Enter Member ID to issue a book: ")
                        member = librarian.verify_member(members, member_id)
                        if member:
                            book_id = int(input("Enter Book ID to issue: "))
                            book = librarian.find_book(library, book_id)
                            if book:
                                librarian.issue_book(library, book, member)
                            else:
                                print("Book not found.")
                        else:
                            print("Member not found.")

                    elif choice == 6:
                        member_id = input("Enter Member ID to return a book: ")
                        member = librarian.verify_member(members, member_id)
                        if member:
                            book_id = int(input("Enter Book ID to return: "))
                            book = librarian.find_book(library, book_id)
                            if book:
                                librarian.return_book(library, book, member)
                            else:
                                print("Book not found.")
                        else:
                            print("Member not found.")

                    elif choice == 7:
                        member_id = input("Enter Member ID: ")
                        member = librarian.verify_member(members, member_id)
                        if member:
                            days_late = int(input("Enter number of days late: "))
                            fine = librarian.calculate_fine(member, days_late)
                            print(f"Fine for {days_late} days late: {fine}")
                        else:
                            print("Member not found.")

                    elif choice == 8:
                        print("Logging out...")
                        break

                    else:
                        print("Invalid choice. Please enter a valid option.")

            else:
                print("Invalid credentials for Librarian.")

        elif select == 2:
            reader_name = input("Enter Reader Name: ")
            reader = library.get_reader(reader_name)

            if reader is None:
                reader = Reader(reader_name)
                library.add_reader(reader)

            print("\t", "_" * 26)
            print("\t\tWelcome ", reader_name)
            print("\t", "_" * 26)

            while True:
                print("\n1. Borrow Book\n2. Return Book\n3. Show Borrowed Books\n4. Purchase Book\n5. Show Purchased Books\n6. Show Author's Books\n7. Logout")
                reader_choice = int(input("Enter your choice: "))

                if reader_choice == 1:
                    library.show_books()
                    book_id = int(input("Enter Book ID to borrow: "))
                    book = next((b for b in library.get_books() if b.book_ID == book_id), None)

                    if book:
                        librarian.issue_book(library, book, reader)
                    else:
                        print(f"No book found with ID: {book_id}")

                elif reader_choice == 2:
                    print('_' * 120)
                    print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s" % ("Book ID", "Title", "Author", "Price", "Status", "Edition", "Date of Purchase", "Owner"))
                    print('_' * 120)
                    reader.show_books()
                    book_id = int(input("Enter Book ID to return: "))
                    book = next((b for b in reader.books if b.book_ID == book_id), None)
                
                    if book:
                        librarian.return_book(library, book, reader)
                    else:
                        print(f"No borrowed book found with ID: {book_id}")
                elif reader_choice == 3:
                    print('_' * 120)
                    print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s" % ("Book ID", "Title", "Author", "Price", "Status", "Edition", "Date of Purchase", "Owner"))
                    print('_' * 120)
                    reader.show_books()

                elif reader_choice == 4:
                    library.show_books()
                    book_id = int(input("Enter Book ID to purchase: "))
                    book = next((b for b in library.get_books() if b.book_ID == book_id), None)

                    if book:
                        reader.purchase_book(book, library)
                    else:
                        print(f"No book found with ID: {book_id}")

                elif reader_choice == 5:
                    reader.show_purchased_books()
                
                elif reader_choice == 6:
                    author_name = input("Enter the author's name: ")
                    if author_name in library.authors:
                        library.authors[author_name].show_books_written()
                    else:
                        print(f"No author found with the name: {author_name}")
                        
                elif reader_choice == 7:
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Please enter a valid option.")

        elif select == 3:
            print("\nManage Members")
            while True:
                print("\n1. Add Member\n2. Show Member Details\n3. Issue Book to Member\n4. Return Book from Member\n5. Pay Bill\n6. Back to Main Menu")
                member_choice = int(input("Enter your choice: "))

                if member_choice == 1:
                    member_id = input("Enter Member ID: ")
                    if member_id in members:
                        print(f"Member with ID {member_id} already exists. Please enter a unique ID.")
                        continue
                    name = input("Enter Member Name: ")
                    member_type = input("Enter Member Type (Faculty/Student): ")
                    date_of_membership = input("Enter Date of Membership: ")
                    max_book_limit = int(input("Enter Max Book Limit: "))
                    address = input("Enter Address: ")
                    phone_number = input("Enter Phone Number: ")

                    member = MemberRecord(member_id, name, member_type, date_of_membership, max_book_limit, address, phone_number)
                    members[member_id] = member
                    reader = Reader(name)
                    library.add_reader(reader)
                    print(f"Member '{name}' added successfully.")
                    
                elif member_choice == 2:
                    member_id = input("Enter Member ID to view details: ")
                    member = members.get(member_id)
                    if member:
                        print(member.get_member())
                    else:
                        print(f"No member found with ID: {member_id}")

                elif member_choice == 3:
                    member_id = input("Enter Member ID to issue a book: ")
                    member = members.get(member_id)
                    if member:
                        library.show_books()
                        book_id = int(input("Enter Book ID to issue: "))
                        book = next((b for b in library.get_books() if b.book_ID == book_id), None)

                        if book:
                            member.inc_book_issued() 
                            librarian.issue_book(library, book, reader)
                        else:
                            print(f"No book found with ID: {book_id}")
                    else:
                        print(f"No member found with ID: {member_id}")

                elif member_choice == 4:
                        member_id = input("Enter Member ID to return a book: ")
                        member = members.get(member_id)
                        if member:
                            if member.books:
                                print("Books currently borrowed:")
                                print('_' * 120)
                                print("%-10s %-15s %-15s %-15s %-15s %-15s %-20s %-15s" % ("Book ID", "Title", "Author", "Price", "Status", "Edition", "Date of Purchase", "Owner"))
                                print('_' * 120)
                                member.show_books()
                                book_id = int(input("Enter Book ID to return: "))
                                book = next((b for b in member.books if b.book_ID == book_id), None)
            
                                if book:
                                    librarian.return_book(library, book, member)
                                    member.dec_book_issued()  
                                    print(f"Book ID {book_id} returned successfully.")
                                else:
                                    print(f"No borrowed book found with ID: {book_id}")
                            else:
                                print("No books currently borrowed by this member.")
                        else:
                            print(f"No member found with ID: {member_id}")

                elif member_choice == 5:
                    member_id = input("Enter Member ID to pay bill: ")
                    member = members.get(member_id)
                    if member:
                        total_amount_due = sum(book.price for book in member.books)
                        print(f"Total amount due: {total_amount_due}")
                        amount = float(input("Enter amount to pay: "))
                        member.pay_bill(amount)
                    else:
                        print(f"No member found with ID: {member_id}")
                
                elif member_choice == 6:
                     break

                else:
                    print("Invalid choice. Please enter a valid option.")

        elif select == 4:
            print("Exiting the program...")
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
