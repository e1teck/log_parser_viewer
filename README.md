# usage

Для работы с приложением перейдите в корень log_parser, 

установите зависимости

```bash
pip install poetry
poetry install --no-root
```

обновите postgres RW_DSN в файле `log_parser/app/config.py`

```postgresql://postgres:postgres@127.0.0.1:55432/log_messages```

запустите скрипт парсера

```bash
python parser.py <путь к файлу лога, по умолчанию out в корне log_parser>
```

запустите fastapi

```bash
uvicorn --host 0.0.0.0 --port 8000 app:app
```

перейдите на страницу `http://0.0.0.0:8000/docs#/log_messages/` для поиска сообщения по адресу

к примеру `shkhta@list.ru`, `tpxmuwr@somehost.ru`, etc...