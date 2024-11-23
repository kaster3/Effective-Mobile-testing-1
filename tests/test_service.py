import unittest
from unittest.mock import MagicMock
from app import Service, LibraryCRUD, Book, BookStatus



class TestService(unittest.TestCase):

    def setUp(self):
        self.mock_library = MagicMock(spec=LibraryCRUD)
        self.service = Service(library=self.mock_library)


    def test_add_book(self):
        self.mock_library.add_book = MagicMock()

        with unittest.mock.patch("builtins.input", side_effect=["Книга 1", "Автор 1", "2023"]):
            self.service.add_book()

        self.mock_library.add_book.assert_called_once_with("Книга 1", "Автор 1", 2023)


    def test_remove_book_success(self):
        book = Book(id=1, title="Книга 1", author="Автор 1", year=2023, status=BookStatus.IN_STOCK)
        self.mock_library.get_book_by_id.return_value = book
        self.mock_library.remove_book = MagicMock()

        with unittest.mock.patch("builtins.input", side_effect=["1"]):
            self.service.remove_book()

        self.mock_library.remove_book.assert_called_once_with(book=book)


    def test_remove_book_not_found(self):
        self.mock_library.get_book_by_id.return_value = None

        with unittest.mock.patch("builtins.input", side_effect=["1"]):
            with unittest.mock.patch("builtins.print") as mocked_print:
                self.service.remove_book()

        mocked_print.assert_called_once_with("Книга с id 1 не найдена.\n")


    def test_get_books_by_params_found(self):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year=2023, status=BookStatus.IN_STOCK)
        book2 = Book(id=2, title="Книга 2", author="Автор 1", year=2022, status=BookStatus.IN_STOCK)
        self.mock_library.get_books.return_value = [book1, book2]

        with unittest.mock.patch("builtins.input", side_effect=["Книга", "Автор 1", ""]):
            with unittest.mock.patch("builtins.print") as mocked_print:
                self.service.get_books_by_params()

        mocked_print.assert_any_call("\nНайденные книги:\n")
        mocked_print.assert_any_call(book1)
        mocked_print.assert_any_call(book2)

    def test_get_books_by_params_not_found(self):
        self.mock_library.get_books.return_value = []

        with unittest.mock.patch("builtins.input", side_effect=["Книга", "Автор 1", ""]):
            with unittest.mock.patch("builtins.print") as mocked_print:
                self.service.get_books_by_params()

        mocked_print.assert_called_once_with("Книги не найдены.")

    def test_get_all_books(self):
        book1 = Book(id=1, title="Книга 1", author="Автор 1", year=2023, status=BookStatus.IN_STOCK)
        book2 = Book(id=2, title="Книга 2", author="Автор 2", year=2022, status=BookStatus.IN_STOCK)
        self.mock_library.books = [book1, book2]

        with unittest.mock.patch("builtins.print") as mocked_print:
            self.service.get_all_books()

        mocked_print.assert_any_call("\nВсе книги в библиотеке:\n")
        mocked_print.assert_any_call(book1)
        mocked_print.assert_any_call(book2)


if __name__ == "__main__":
    unittest.main()