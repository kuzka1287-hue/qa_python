import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Фикстура создаёт новый экземпляр BooksCollector для каждого теста."""
    return BooksCollector()

class TestBooksCollector:

    # Пример теста: добавление двух книг (исправлен вызов get_books_genre)
    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # Параметризованный тест для add_new_book: проверка граничных условий длины имени
    @pytest.mark.parametrize("name, should_be_added", [
        ("", False),           # пустое имя – не добавляется
        ("a" * 40, True),      # ровно 40 символов – добавляется
        ("a" * 41, False),     # 41 символ – не добавляется
        ("Обычное имя", True)  # обычное имя – добавляется
    ])
    def test_add_new_book_name_validation(self, collector, name, should_be_added):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == should_be_added

    # Тест установки жанра существующей книге
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    # Тест установки жанра несуществующей книге
    def test_set_book_genre_nonexistent_book(self, collector):
        collector.set_book_genre('Нет такой', 'Комедии')
        assert collector.get_book_genre('Нет такой') is None

    # Параметризованный тест для недопустимых жанров
    @pytest.mark.parametrize("invalid_genre", ["Драма", "", "Триллер", "Роман"])
    def test_set_book_genre_invalid_genre_not_set(self, collector, invalid_genre):
        collector.add_new_book('Матильда')
        collector.set_book_genre('Матильда', invalid_genre)
        assert collector.get_book_genre('Матильда') == ""

    # Тест get_book_genre для отсутствующей книги
    def test_get_book_genre_returns_none_for_missing(self, collector):
        assert collector.get_book_genre("Отсутствует") is None

    # Тест получения книг определённого жанра
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        collector.set_book_genre('Книга1', 'Ужасы')
        collector.set_book_genre('Книга2', 'Комедии')
        assert collector.get_books_with_specific_genre('Ужасы') == ['Книга1']

    # Тест получения словаря books_genre
    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book('Книга')
        assert isinstance(collector.get_books_genre(), dict)
        assert 'Книга' in collector.get_books_genre()

    # Тест получения книг для детей (исключая возрастные жанры)
    def test_get_books_for_children_excludes_age_rated(self, collector):
        collector.add_new_book('Ужастик')
        collector.add_new_book('Мульт')
        collector.set_book_genre('Ужастик', 'Ужасы')      # возрастной рейтинг
        collector.set_book_genre('Мульт', 'Мультфильмы')  # без рейтинга
        assert collector.get_books_for_children() == ['Мульт']

    # Тест добавления книги в избранное
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book('Избранная')
        collector.add_book_in_favorites('Избранная')
        assert 'Избранная' in collector.get_list_of_favorites_books()

    # Тест добавления одной и той же книги в избранное дважды (не дублируется)
    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book('Дубль')
        collector.add_book_in_favorites('Дубль')
        collector.add_book_in_favorites('Дубль')
        assert collector.get_list_of_favorites_books().count('Дубль') == 1

    # Тест добавления несуществующей книги в избранное
    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites('Нет в словаре')
        assert collector.get_list_of_favorites_books() == []

    # Тест удаления книги из избранного
    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()

    # Тест удаления книги, которой нет в избранном (без ошибки)
    def test_delete_book_not_in_favorites_no_error(self, collector):
        collector.delete_book_from_favorites('Отсутствует')
        assert collector.get_list_of_favorites_books() == []

    # Тест получения списка избранных книг (всегда список)
    def test_get_list_of_favorites_books_returns_list(self, collector):
        assert isinstance(collector.get_list_of_favorites_books(), list)
