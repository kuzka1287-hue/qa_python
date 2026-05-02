import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Фикстура создаёт новый экземпляр BooksCollector для каждого теста."""
    return BooksCollector()

class TestBooksCollector:

    # Тест добавления двух книг
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Параметризованный тест для граничных условий: длина имени
    @pytest.mark.parametrize("name, expected", [
        ("", False),         # пустое имя – не добавится
        ("a" * 40, True),    # ровно 40 символов – добавится
        ("a" * 41, False),   # 41 символ – не добавится
        ("Нормальное имя", True)
    ])
    def test_add_new_book_name_length(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    # Тест: одна и та же книга добавляется только один раз
    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Дубль")
        collector.add_new_book("Дубль")
        assert len(collector.get_books_genre()) == 1
        assert "Дубль" in collector.get_books_genre()

    # Тест get_book_genre для отсутствующей книги
    def test_get_book_genre_missing(self, collector):
        assert collector.get_book_genre("Нет такой") is None

    # Тест установки жанра существующей книге
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_book_genre("Дюна") == "Фантастика"

    # Тест установки жанра несуществующей книге
    def test_set_book_genre_nonexistent(self, collector):
        collector.set_book_genre("Нет такой", "Комедии")
        assert collector.get_book_genre("Нет такой") is None

    # Параметризованный тест: установка недопустимого жанра
    @pytest.mark.parametrize("invalid_genre", ["Драма", "", "Триллер"])
    def test_set_book_genre_invalid(self, collector, invalid_genre):
        collector.add_new_book("Матильда")
        collector.set_book_genre("Матильда", invalid_genre)
        assert collector.get_book_genre("Матильда") == ""

    # Тест get_books_with_specific_genre
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Ужасы")
        collector.set_book_genre("Книга2", "Комедии")

        # Проверка для существующего жанра
        assert collector.get_books_with_specific_genre("Ужасы") == ["Книга1"]
        # Проверка для несуществующего жанра
        assert collector.get_books_with_specific_genre("Фэнтези") == []

    # Тест get_books_genre (покрытие метода)
    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга")
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert "Книга" in books_genre

    # Тест get_books_for_children (исключает возрастные жанры)
    def test_get_books_for_children(self, collector):
        collector.add_new_book("Ужастик")
        collector.add_new_book("Мульт")
        collector.set_book_genre("Ужастик", "Ужасы")    # возрастной рейтинг
        collector.set_book_genre("Мульт", "Мультфильмы") # без рейтинга
        assert collector.get_books_for_children() == ["Мульт"]

    # Тест add_book_in_favorites: успешное добавление
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Избранная")
        collector.add_book_in_favorites("Избранная")
        assert "Избранная" in collector.get_list_of_favorites_books()

    # Тест добавления в избранное дубликата
    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")
        assert collector.get_list_of_favorites_books().count("Дубль") == 1

    # Тест добавления несуществующей книги в избранное
    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites("Отсутствует")
        assert collector.get_list_of_favorites_books() == []

    # Тест delete_book_from_favorites: успешное удаление
    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.get_list_of_favorites_books()

    # Тест удаления книги, которой нет в избранном (без ошибок)
    def test_delete_book_not_in_favorites(self, collector):
        collector.delete_book_from_favorites("Нет в избранном")
        assert collector.get_list_of_favorites_books() == []

    # Тест get_list_of_favorites_books всегда возвращает список
    def test_get_list_of_favorites_books_returns_list(self, collector):
        assert isinstance(collector.get_list_of_favorites_books(), list)

