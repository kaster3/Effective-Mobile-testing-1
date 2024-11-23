import unittest
from unittest.mock import MagicMock
from app import LibraryCRUD, Book, BookStatus


class TestLibraryCRUD(unittest.TestCase):

    def setUp(self):
        self.mock_storage = MagicMock()
        self.library = LibraryCRUD(storage=self.mock_storage)

        self.book1 = Book(id=1, title="1984", author="George Orwell", year=1949, status=BookStatus.IN_STOCK)
        self.book2 = Book(id=2, title="Brave New World", author="Aldous Huxley", year=1932, status=BookStatus.IN_STOCK)

        self.library.books = [self.book1, self.book2]
        self.mock_storage.load_books.return_value = self.library.books

    def test_get_book_by_id(self):
        book = self.library.get_book_by_id(1)
        self.assertEqual(book, self.book1)

        book = self.library.get_book_by_id(3)
        self.assertIsNone(book)

    def test_add_book(self):
        self.library.add_book("Fahrenheit 451", "Ray Bradbury", 1953)

        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[-1].title, "Fahrenheit 451")

        self.mock_storage.save_books.assert_called_once_with(books=self.library.books)

    def test_remove_book(self):
        self.library.remove_book(self.book1)

        self.assertEqual(len(self.library.books), 1)
        self.assertNotIn(self.book1, self.library.books)

        self.mock_storage.save_books.assert_called_once_with(books=self.library.books)

    def test_get_books_with_title_filter(self):
        result = self.library.get_books(title="1984")
        self.assertIn(self.book1, result)
        self.assertNotIn(self.book2, result)

    def test_change_status(self):
        self.library.change_status(self.book1)

        self.assertEqual(self.book1.status, BookStatus.CHECKED_OUT)

        self.mock_storage.save_books.assert_called_once_with(books=self.library.books)


if __name__ == '__main__':
    unittest.main()