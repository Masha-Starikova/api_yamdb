# api_yamdb
api_yamdb
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Masha-Starikova/api_yamdb.git
```

```
cd api_yamdb/
```

    Cоздать и активировать виртуальное окружение:

    ```
    python -m venv venv
    ```

    ```
    source venv/Scripts/activate
    ```

    ```
    python -m pip install --upgrade pip
    ```

    Установить зависимости из файла requirements.txt:

    ```
    pip install -r requirements.txt
    ```

    Выполнить миграции:

    ```
    python manage.py migrate
    ```

    Запустить проект:

    ```
    python manage.py runserver
    ```
