from .storage import Storage
from .model import Book, BookStatus


class LibraryCRUD:
    """
    Класс LibraryCRUD предназначен для прямого выполнения CRUD операций, а также работает
    с хранилищем книг, сохраняя туда данные и вытаскивая

    Args:
        self.storage: Класс хранилище
        self.books: Список книг, загруженных из json файла
    """
    def __init__(self, storage: Storage) -> None:
        self.storage: Storage = storage
        self.books: list[Book | None] = self.storage.load_books()


    def get_book_by_id(self, book_id: int | None) -> Book | None:
        """
        Метод для получения книги по ее id
        """
        for book in self.books:
            if book.id == book_id:
                return book


    def add_book(self, title: str, author: str, year: int) -> None:
        """
        Метод для добавления новой книги и ее сохранения на основе полученных параметров
        с автоматической генерации уникального id книги
        """
        # Генерация уникального id
        book_id: int = self.books[-1].id + 1 if self.books else 1
        new_book: Book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.storage.save_books(books=self.books)


    def remove_book(self, book: Book) -> None:
        """
        Метод удаления книги предварительно, которая была найдена
        """
        self.books.remove(book)
        self.storage.save_books(books=self.books)


    def get_books(
            self,
            title: str | None = None,
            author: str | None = None,
            year: int | None = None,
    ) -> set[Book] | list[Book | None]:
        """
        Метод получения, неповторяющихся, книг, по переданным параметрам
        """
        all_books: list[Book | None] = self.books
        result: set[Book | None] = set()

        if title:
            result.update([book for book in all_books if title.lower() in book.title.lower()])
        if author:
            result.update([book for book in all_books if author.lower() in book.author.lower()])
        if year:
            result.update([book for book in all_books if book.year == year])

        return result if result else all_books


    def change_status(self, book: Book) -> None:
        """
        Метод меняющий состояние статуса на противоположный у книги, которая была заранее найдена
        """
        if book.status == BookStatus.IN_STOCK:
            book.status = BookStatus.CHECKED_OUT
        else:
            book.status = BookStatus.IN_STOCK
        self.storage.save_books(books=self.books)
