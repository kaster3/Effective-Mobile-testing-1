from dataclasses import dataclass
from enum import Enum


class BookStatus(Enum):
    """
    Клас представляющий статус книг (в наличии, выдана), для более удобного взаимодействия
    и уменьшения шанса на ошибку
    """
    IN_STOCK = "В наличии"
    CHECKED_OUT = "Выдана"

    @staticmethod
    def from_value(value: str) -> "BookStatus":
        """
        Метод для получения статуса книги по его значению, для того чтобы json корректно работал с Enum
        """
        for status in BookStatus:
            if status.value == value:
                return status
        return BookStatus.IN_STOCK


@dataclass
class Book:
    """Основная бизнес сущность с которой будут выполняться все CRUD операции"""
    id: int
    title: str
    author: str
    year: int
    status: BookStatus = BookStatus.IN_STOCK


    def __str__(self):
        """
        Метод для вывода информации о книге в удобном виде
        """
        return (
            f"Книга №{self.id}\nНазвание: {self.title}\nАвтор:  {self.author}\n"
            f"Год издания: {self.year}\nСтатус выдачи: {self.status.value}\n"
        )


    def to_dict(self):
        """
        Метод для преобразования экземпляра книги в словарь так как json не умеет работать с классом Enum
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status.value
        }


    def __hash__(self):
        return hash((self.id, self.title, self.author, self.year, self.status))

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented

        return (self.id, self.title, self.author, self.year, self.status) == \
            (other.id, other.title, other.author, other.year, other.status)