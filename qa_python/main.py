import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Фикстура возвращает новый экземпляр BooksCollector для каждого теста."""
    return BooksCollector()

class TestBooksCollector:

    # ---------- add_new_book ----------
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Книга")
        assert "Книга" in collector.get_books_genre()
        assert collector.get_book_genre("Книга") == ""

    @pytest.mark.parametrize("name, expected", [
        ("", False),
        ("a" * 40, True),
        ("a" * 41, False),
        ("Обычное имя", True)
    ])
    def test_add_new_book_name_validation(self, collector, name, expected):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book("Дубль")
        collector.add_new_book("Дубль")
        assert len(collector.get_books_genre()) == 1
        assert "Дубль" in collector.get_books_genre()

    # ---------- set_book_genre & get_book_genre ----------
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        assert collector.get_book_genre("Дюна") == "Фантастика"

    def test_set_book_genre_nonexistent_book(self, collector):
        collector.set_book_genre("Нет такой", "Комедии")
        assert collector.get_book_genre("Нет такой") is None

    @pytest.mark.parametrize("invalid_genre", ["Драма", "", "Триллер"])
    def test_set_book_genre_invalid_genre(self, collector, invalid_genre):
        collector.add_new_book("Матильда")
        collector.set_book_genre("Матильда", invalid_genre)
        assert collector.get_book_genre("Матильда") == ""

    def test_get_book_genre_missing(self, collector):
        assert collector.get_book_genre("Отсутствует") is None

    # ---------- get_books_with_specific_genre ----------
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Ужасы")
        collector.set_book_genre("Книга2", "Комедии")
        assert collector.get_books_with_specific_genre("Ужасы") == ["Книга1"]

    def test_get_books_with_specific_genre_empty(self, collector):
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # ---------- get_books_genre ----------
    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга")
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)
        assert "Книга" in books_genre

    # ---------- get_books_for_children ----------
    def test_get_books_for_children_excludes_age_rated(self, collector):
        collector.add_new_book("Ужастик")
        collector.add_new_book("Мульт")
        collector.set_book_genre("Ужастик", "Ужасы")   # возрастной рейтинг
        collector.set_book_genre("Мульт", "Мультфильмы")
        assert collector.get_books_for_children() == ["Мульт"]

    def test_get_books_for_children_no_genre(self, collector):
        collector.add_new_book("Без жанра")
        assert collector.get_books_for_children() == []

    # ---------- favorites ----------
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book("Избранная")
        collector.add_book_in_favorites("Избранная")
        assert "Избранная" in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book("Дубль")
        collector.add_book_in_favorites("Дубль")
        collector.add_book_in_favorites("Дубль")
        assert collector.get_list_of_favorites_books().count("Дубль") == 1

    def test_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites("Отсутствует")
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.get_list_of_favorites_books()

    def test_delete_book_not_in_favorites(self, collector):
        collector.delete_book_from_favorites("Нет в избранном")
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_returns_list(self, collector):
        assert isinstance(collector.get_list_of_favorites_books(), list)
