from app.library import LibraryCRUD
from app.model import Book


class Service:
    """
        Класс Service предназначен для управления основной логикой выполнения выбранной
        пользователем операции, ветвление логики, отображения сообщений и вызов соответствующих
        методов у класса такими как добавление, удаление, поиск и изменение статуса книг (CRUD)
        через класс LibraryCRUD.

        Args:
            library (LibraryCRUD): экземпляр класса LibraryCRUD,
            в котором будут выполняться основные CRUD операции
    """
    def __init__(self, library: LibraryCRUD) -> None:
        self.library: LibraryCRUD = library


    def add_book(self) -> None:
        """
        Метод для получения параметров книги от пользователя и передаче их методу создания в LibraryCRUD
        """
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = int(input("Введите год издания: "))
        self.library.add_book(title, author, year)


    def remove_book(self) -> None:
        """
        Метод для получения ID книги от пользователя и вызов метода удаления у LibraryCRUD,
        если такая книга есть в библиотеке.
        """
        book_id = int(input("Введите ID книги для удаления: "))
        book = self.library.get_book_by_id(book_id)
        if book:
            self.library.remove_book(book=book)
            print(f"Книга с id {book_id} успешно удалена.\n")
        else:
            print(f"Книга с id {book_id} не найдена.\n")


    def get_books_by_params(self):
        """
        Метод для получения параметров поиска книг от пользователя и вызова
        метода получения книг у LibraryCRUD с соответствующими параметрами,
        если множество не пустое.
        """
        title: str = input("Введите название книги для поиска (или оставьте пустым): ")
        author: str = input("Введите автора книги для поиска (или оставьте пустым): ")
        year_input: str | None = input("Введите год издания для поиска (или оставьте пустым): ")
        try:
            year: int | None = int(year_input) if year_input else None
        except ValueError:
            print(f"\n!!!Год должен быть целым число или пустым значение!!!\n")
            return

        results: set[Book | None] | list [Book | None] = self.library.get_books(title, author, year)
        if results:
            print("\nНайденные книги:\n")
            for book in results:
                print(book)
        else:
            print("Книги не найдены.")


    def get_all_books(self) -> None:
        """Получение всех книг через LibraryCRUD"""
        books: list[Book | None] = self.library.books
        if books:
            print("\nВсе книги в библиотеке:\n")
            for book in books:
                print(book)
        else:
            print("Библиотека пуста.\n")


    def change_status(self) -> None:
        """
        Метод, который получает BOOK по ID книги введенным пользователем и если она существует,
        то вызываем метод изменения статуса книги через LibraryCRUD
        """
        book_id = int(input("Введите ID книги для изменения статуса: "))
        book = self.library.get_book_by_id(book_id)
        if book:
            new_status = input(
                f"Текущий статуc книги '{book.title}' - '{book.status.value}',"
                f" хотите поменять?\n1. Да\n2. Нет\nВыберите действие: ")
            if new_status == '1':
                self.library.change_status(book=book)
        else:
            print(f"Книга с id {book_id} не найдена")


    @staticmethod
    def get_choice() -> str:
        """
            Статический метод для отображения панели управления и приема выбора пользователя
        """
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход\n")

        choice = input("Выберите действие: ")
        return choice