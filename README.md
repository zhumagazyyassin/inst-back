# Instagram Clone (Backend)

Бұл жоба Django Rest Framework (DRF) көмегімен жасалған Instagram клонының серверлік бөлігі (backend).

## Қолданылған технологиялар
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Simple JWT (Аутентификация үшін)

## Орнату және іске қосу

1.  Репозиторийді клондау:
    ```bash
    git clone [https://github.com/zhumagazyyassin/instagram-clone.git](https://github.com/zhumagazyyassin/instagram-clone.git)
    ```
2.  Виртуалды ортаны құру және пакеттерді орнату:
    ```bash
    pip install -r requirements.txt
    ```
3.  Дерекқор миграцияларын жасау:
    ```bash
    python manage.py migrate
    ```
4.  Серверді іске қосу:
    ```bash
    python manage.py runserver
    ```
