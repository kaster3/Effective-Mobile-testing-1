import unittest
import json
import os
import tempfile


from app import Book, BookStatus, Storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
        self.storage = Storage()
        self.storage.storage_file = self.test_file
        self.test_books = [
            Book(id=1, title="Book One", author="Author A", year=2021, status=BookStatus.IN_STOCK),
            Book(id=2, title="Book Two", author="Author B", year=2022, status=BookStatus.CHECKED_OUT)
        ]


    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


    def test_initialization(self):
        self.assertEqual(self.storage.storage_file, self.test_file)


    def test_save_books(self):
        self.storage.save_books(self.test_books)
        with open(self.test_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["title"], "Book One")
            self.assertEqual(data[0]["year"], 2021)
            self.assertEqual(data[1]["title"], "Book Two")
            self.assertEqual(data[1]["year"], 2022)


    def test_load_books(self):
        self.storage.save_books(self.test_books)
        loaded_books = self.storage.load_books()
        self.assertEqual(len(loaded_books), 2)
        self.assertEqual(loaded_books[0].title, "Book One")
        self.assertEqual(loaded_books[0].year, 2021)
        self.assertEqual(loaded_books[1].title, "Book Two")
        self.assertEqual(loaded_books[1].year, 2022)


    def test_load_books_file_not_found(self):
        os.remove(self.test_file)
        loaded_books = self.storage.load_books()
        self.assertEqual(loaded_books, [])


    def test_load_books_json_decode_error(self):
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("Invalid JSON")
        loaded_books = self.storage.load_books()
        self.assertEqual(loaded_books, [])


    def test_load_books_key_error(self):
        with open(self.test_file, "w", encoding="utf-8") as file:
            json.dump([{"id": 1, "title": "Book One", "author": "Author A", "year": 2021}], file)
        loaded_books = self.storage.load_books()
        self.assertEqual(len(loaded_books), 0)


if __name__ == "__main__":
    unittest.main()