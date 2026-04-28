import pytest
from main import BooksCollector

class TestBooksCollector:

    # пример теста (уже есть)
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2   # замените на get_books_rating если нужно

    # 1. Тест добавления книги с пустым именем
    def test_add_new_book_empty_name_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('')
        assert len(collector.get_books_genre()) == 0

    # 2. Тест добавления книги с именем длиной 40 символов (граница)
    def test_add_new_book_max_length_name_added(self):
        collector = BooksCollector()
        long_name = 'a' * 40
        collector.add_new_book(long_name)
        assert long_name in collector.get_books_genre()

    # 3. Тест добавления книги с именем длиной 41 символ (не добавляется)
    def test_add_new_book_too_long_name_not_added(self):
        collector = BooksCollector()
        too_long_name = 'a' * 41
        collector.add_new_book(too_long_name)
        assert too_long_name not in collector.get_books_genre()

    # 4. Тест установки жанра существующей книге
    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    # 5. Тест установки жанра несуществующей книге (не меняет словарь)
    def test_set_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Нет такой', 'Комедии')
        assert collector.get_book_genre('Нет такой') is None

    # 6. Тест установки недопустимого жанра
    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Матильда')
        collector.set_book_genre('Матильда', 'Драма')  # Драмы нет в списке genre
        assert collector.get_book_genre('Матильда') == ''

    # 7. Тест получения книг определённого жанра
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')
        collector.set_book_genre('Книга1', 'Ужасы')
        collector.set_book_genre('Книга2', 'Комедии')
        assert collector.get_books_with_specific_genre('Ужасы') == ['Книга1']

    # 8. Тест получения списка книг для детей (без возрастного рейтинга)
    def test_get_books_for_children_excludes_age_rated(self):
        collector = BooksCollector()
        collector.add_new_book('Ужастик')
        collector.add_new_book('Мульт')
        collector.set_book_genre('Ужастик', 'Ужасы')
        collector.set_book_genre('Мульт', 'Мультфильмы')
        assert collector.get_books_for_children() == ['Мульт']

    # 9. Тест добавления книги в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Избранная')
        collector.add_book_in_favorites('Избранная')
        assert 'Избранная' in collector.get_list_of_favorites_books()

    # 10. Тест добавления одной и той же книги в избранное дважды (не дублируется)
    def test_add_book_in_favorites_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Дубль')
        collector.add_book_in_favorites('Дубль')
        collector.add_book_in_favorites('Дубль')
        assert collector.get_list_of_favorites_books().count('Дубль') == 1

    # 11. Тест удаления книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()
