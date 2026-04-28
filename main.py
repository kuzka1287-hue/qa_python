import pytest
from main import BooksCollector  # предполагается, что класс в файле main.py

@pytest.fixture
def collector():
    """Фикстура создаёт новый экземпляр BooksCollector для каждого теста."""
    return BooksCollector()

# 1. Тесты для add_new_book
class TestAddNewBook:
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_books_genre()
        assert collector.get_book_genre("Гарри Поттер") == ""

    @pytest.mark.parametrize("name", ["", "a" * 41, "a" * 100])
    def test_add_new_book_invalid_name_not_added(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Книга")
        collector.add_new_book("Книга")
        assert len(collector.get_books_genre()) == 1

# 2. Тесты для set_book_genre
class TestSetBookGenre:
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_book_genre("Дюна") == "Фантастика"

    def test_set_book_genre_for_nonexistent_book(self, collector):
        collector.set_book_genre("Нет такой", "Комедии")
        assert collector.get_book_genre("Нет такой") is None

    @pytest.mark.parametrize("invalid_genre", ["Драма", "", "Боевик"])
    def test_set_book_genre_invalid_genre_not_set(self, collector, invalid_genre):
        collector.add_new_book("Матильда")
        collector.set_book_genre("Матильда", invalid_genre)
        assert collector.get_book_genre("Матильда") == ""

# 3. Тест для get_book_genre (уже частично проверен выше, но добавим отдельно)
def test_get_book_genre_returns_none_for_missing_book(collector):
    assert collector.get_book_genre("Отсутствует") is None

# 4. Тесты для get_books_with_specific_genre
class TestGetBooksWithSpecificGenre:
    def test_get_books_with_specific_genre_multiple_books(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга1", "Ужасы")
        collector.set_book_genre("Книга2", "Детективы")
        collector.set_book_genre("Книга3", "Ужасы")
        assert collector.get_books_with_specific_genre("Ужасы") == ["Книга1", "Книга3"]

    def test_get_books_with_specific_genre_no_books(self, collector):
        assert collector.get_books_with_specific_genre("Фантастика") == []

    def test_get_books_with_specific_genre_nonexistent_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Комедии")
        assert collector.get_books_with_specific_genre("Драма") == []

# 5. Тест для get_books_genre
def test_get_books_genre_returns_dict(collector):
    collector.add_new_book("Книга")
    assert isinstance(collector.get_books_genre(), dict)
    assert "Книга" in collector.get_books_genre()

# 6. Тесты для get_books_for_children
class TestGetBooksForChildren:
    def test_books_for_children_excludes_age_rated_genres(self, collector):
        collector.add_new_book("Ужастик")
        collector.add_new_book("Мульт")
        collector.set_book_genre("Ужастик", "Ужасы")
        collector.set_book_genre("Мульт", "Мультфильмы")
        assert collector.get_books_for_children() == ["Мульт"]

    def test_books_for_children_only_with_valid_genre(self, collector):
        collector.add_new_book("Без жанра")
        # книга есть, но жанр не установлен – не попадёт в детские
        assert collector.get_books_for_children() == []

# 7. Тесты для add_book_in_favorites
class TestAddBookInFavorites:
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Избранная")
        collector.add_book_in_favorites("Избранная")
        assert "Избранная" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate_not_added(self, collector):
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")
        assert collector.get_list_of_favorites_books().count("Дубль") == 1

    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites("Нет в словаре")
        assert collector.get_list_of_favorites_books() == []

# 8. Тесты для delete_book_from_favorites
class TestDeleteBookFromFavorites:
    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.get_list_of_favorites_books()

    def test_delete_book_not_in_favorites_no_error(self, collector):
        collector.delete_book_from_favorites("Отсутствует")
        assert collector.get_list_of_favorites_books() == []

# 9. Тест для get_list_of_favorites_books (возвращает список)
def test_get_list_of_favorites_books_returns_list(collector):
    assert isinstance(collector.get_list_of_favorites_books(), list)
