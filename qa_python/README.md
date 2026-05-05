# qa_python
# Тесты для BooksCollector

В этом проекте реализован набор автотестов для класса `BooksCollector` с использованием библиотеки `pytest`.  
Класс `BooksCollector` предназначен для управления коллекцией книг: добавление книг, установка жанров, фильтрация по жанрам, получение списка книг для детей, работа с избранным.

## Реализованные тесты

### 1. `add_new_book` – добавление новой книги
- `test_add_new_book_success` – проверяет, что книга добавляется корректно.
- `test_add_new_book_name_validation` (параметризованный) – проверяет граничные значения длины названия (пустая строка, 40 символов, 41 символ, обычное имя).
- `test_add_new_book_duplicate_not_added` – проверяет, что одну и ту же книгу нельзя добавить дважды.

### 2. `set_book_genre` – установка жанра книге
- `test_set_book_genre_valid` – успешная установка допустимого жанра.
- `test_set_book_genre_nonexistent_book` – попытка установить жанр несуществующей книге игнорируется.
- `test_set_book_genre_invalid_genre` (параметризованный) – попытка установить недопустимый (отсутствующий в списке) жанр не меняет жанр книги.

### 3. `get_book_genre` – получение жанра по названию
- `test_get_book_genre_missing` – для отсутствующей книги возвращается `None`.

### 4. `get_books_with_specific_genre` – получение списка книг по жанру
- `test_get_books_with_specific_genre` – возвращает список книг с указанным жанром.
- `test_get_books_with_specific_genre_empty` – если книг с таким жанром нет, возвращается пустой список.

### 5. `get_books_genre` – получение всего словаря книг
- `test_get_books_genre_returns_dict` – проверяет, что метод возвращает словарь, содержащий добавленные книги.

### 6. `get_books_for_children` – получение книг без возрастного рейтинга
- `test_get_books_for_children_excludes_age_rated` – книги с жанром из `genre_age_rating` (Ужасы, Детективы) не попадают в список для детей.
- `test_get_books_for_children_no_genre` – книга без установленного жанра не включается в детский список.

### 7. `add_book_in_favorites` – добавление в избранное
- `test_add_book_in_favorites_success` – успешное добавление существующей книги в избранное.
- `test_add_book_in_favorites_duplicate` – повторное добавление той же книги не создаёт дубликата.
- `test_add_nonexistent_book_to_favorites` – попытка добавить несуществующую книгу игнорируется.

### 8. `delete_book_from_favorites` – удаление из избранного
- `test_delete_book_from_favorites_success` – книга успешно удаляется из избранного.
- `test_delete_book_not_in_favorites` – удаление книги, которой нет в избранном, не вызывает ошибок.

### 9. `get_list_of_favorites_books` – получение списка избранного
- `test_get_list_of_favorites_books_returns_list` – метод всегда возвращает список (даже пустой).

## Запуск тестов

