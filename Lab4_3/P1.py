"""
Panhathai Suporn
683040496-5
P1
"""

from datetime import datetime

class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False

    def get_status(self):
        return "Checked out" if self._checked_out else "Available"

    def check_out(self):
        if not self._checked_out:
            self._checked_out = True
            return True
        return False

    # add method
    def return_item(self):
        if self._checked_out:
            self._checked_out = False
            return True
        return False

    def display_info(self):
        print(f"Title: {self.title}")
        print(f"ID: {self._id}")
        print(f"Status: {self.get_status()}")


# implement 3 classes here

# Book Class
class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0  # non-parameter instance attribute

    def set_pages(self, pages):
        self.pages_count = pages

    def display_info(self):
        if self.check_out():
            status = "Checked Out"
        else:
            status = "Avaliable"
        print(f"Title: {self.title}")
        print(f"Status: {self.get_status()}")
        print(f"Author: {self.author}")
        print(f"Pages: {self.pages_count}")
      



# TextBook Class
class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade

    def display_info(self):
        super().display_info()
        print(f"Subject: {self.subject}")
        print(f"Grade Level: {self.grade_level}")


# Magazine Class
class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue):
        super().__init__(title, item_id)
        self.issue = issue

        self.month = datetime.now().month
        self.year = datetime.now().year

    def display_info(self):
        super().display_info()
        print(f"Issue Number: {self.issue}")
        print(f"Month: {self.month}")
        print(f"Year: {self.year}")
  



