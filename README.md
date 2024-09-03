# Blogicum

Перед вами проект социальной сети для публикации личных дневников.

Это сайт, на котором пользователь может публиковать свои записи («посты»), а другие пользователи могут просматривать публикации и оставлять на них комментарии.

По желанию, пользователь может отредактировать или удалить свои публикации или комментарии.

Для удобства управления сайтом, админ-зона доработана и переведена на русский язык.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```shell
git clone git@github.com:ivanhom/django_sprint4.git
```

```shell
cd django_sprint4
```
<br>

Cоздать и активировать виртуальное окружение:

- Для linux/mac:
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
- Для Windows:
    ```shell
    python -m venv venv
    .\venv\Scripts\activate
    ```

Установить зависимости из файла requirements.txt:

```shell
python -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

Перейти в дирректорию `blogicum` и выполнить миграции:

```shell
cd blogicum
```
```shell
python manage.py migrate
```

Наполнить базу данных тестовыми данными:

```shell
python manage.py loaddata db.json
```

Запустить проект:

```shell
python manage.py runserver
```

Далее можно перейти на [главную страницу](http://127.0.0.1:8000/) и опробовать функционал
