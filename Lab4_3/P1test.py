"""
Panhathai Suporn
683040496-5
P1
"""

from P1 import Book, TextBook, Magazine
# Test Program

if __name__ == "__main__":
    print("=== Book ===")
    book = Book("Harry Potter", "B001", "J.K. Rowling")
    # book.set_pages(464)
    print(book.get_status())
    book.check_out()
    print(book.get_status())
    book.return_item()
    # print(book.get_status())
    book.set_pages(100)
    book.display_info()
    
    # book.check_out()
    print()

    print("=== TextBook ===")
    textbook = TextBook("Physics", "T101", "Serway", "Science", "Grade 10")
    textbook.set_pages(500)
    textbook.display_info()
    textbook.check_out()
    print()

    print("=== Magazine ===")
    magazine = Magazine("National Geographic", "M201", 120)
    magazine.display_info()
    magazine.check_out()
