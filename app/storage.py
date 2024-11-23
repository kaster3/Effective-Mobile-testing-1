import json

from app.model import BookStatus, Book



class Storage:
    """
        Класс Storage предназначен для управления хранением и сохранением книг в формате JSON.

        Args:
            self.storage_file (str): имя файла для хранения книг
    """
    def __init__(self) -> None:
        self.storage_file = "books.json"

    def save_books(self, books) -> None:
        """
        Метод для сохранения списка книг в формате JSON в указанный файл или созднание этого файла при
        его отсутствие
        """
        with open(self.storage_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)
        print("Изменения сохранены в файл.\n")


    def load_books(self) -> list[Book | None]:
        """
        Метод для загрузки книг из файла JSON и преобразования их в список моделей Book
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                books_data = json.load(file)

                # Преобразование словаря в модель Book и создание списка книг
                # Возможно выглядит сложно потому, что обязательно нужно привести статус в Enum
                unsorted_books: list[Book | None] = [
                    Book(
                        **{**data, "status": BookStatus.from_value(data["status"])}
                    )
                    for data in books_data
                ]
                # Сортировка книг по id, на случай, если книги в файле были переставлены,
                # так как будет генерироваться неправильный id, он генерируется: books[-1] + 1
                return sorted(unsorted_books, key=lambda book: book.id)

        except FileNotFoundError:
            return []
        except json.JSONDecodeError as exc:
            print(f"Ошибка при загрузке книг из файла: {exc}")
            return []
        except KeyError as exc:
            print(f"Ошибка преобразования статуса книги: {exc}")
            return []
