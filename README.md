# api_yamdb
api_yamdb
### Разработчики:

```
Группа 9.
https://github.com/Sekhniev
https://github.com/Elmiraz-ship-it
https://github.com/Masha-Starikova
```

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
