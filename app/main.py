from service_layer import Service
from library import LibraryCRUD
from storage import Storage


def main() -> None:
    """
    Главный цикл приложения, который обрабатывает взаимодействие с пользователем и вызывает
    соответствующие методы у класса Service, выполняя основную бизнес логику
    """
    storage: Storage = Storage()
    library: LibraryCRUD = LibraryCRUD(storage=storage)
    service: Service = Service(library=library)

    while True:
        choice = service.get_choice()

        if choice == "1":
            service.add_book()

        elif choice == "2":
            service.remove_book()

        elif choice == "3":
            service.get_books_by_params()

        elif choice == "4":
            service.get_all_books()

        elif choice == "5":
            service.change_status()

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Выбери число от 1 до 6 включительно.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Кажется это операция не работает, свяжитесь с разработчиком.\n{exc.__class__.__name__} -> {exc}")