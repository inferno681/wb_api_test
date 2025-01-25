[![main](https://github.com/inferno681/wb_api_test/actions/workflows/main.yaml/badge.svg)](https://github.com/inferno681/wb_api_test/actions/workflows/main.yaml)
[![codecov](https://codecov.io/gh/inferno681/wb_api_test/graph/badge.svg?token=J9AQAQ2K2H)](https://codecov.io/gh/inferno681/wb_api_test)

# WB Collection Service

Сервис отслеживания информации о товарах.

<details><summary><h2>Реализованые возможности</h2></summary>
- Запуск загрузки информации о товаре в базу данных.
- Запуск загрузки информации о товаре в базу данных с обновлением каждые 30 минут.
- Остановка обновления информации о товаре в базе данных.
</details>

<details><summary><h2>Запуск проекта</h2></summary>
1. Клонируйте репозиторий, создайте виртуальное окружение и активируйте его.

2. Установите poetry:
```bash
pip install poetry
```
3. Установите зависимости:
```bash
poetry install
```
Можно использовать ключ "--only main", если не нужно запускать тесты или линтеры.

4. Создайте .env файл с данными для подключения к бд:
```
POSTGRES_PASSWORD=password
```
5. Все настройки приложения находятся в файле src/config/config.yaml. Измените значение host раздела db на "localhost".

6. Базу данных можно запустить в контейнере:
```bash
docker compose -f ./infra/docker-compose-dev.yaml up -d
```
7. Запустите приложение:
```bash
export PYTHONPATH=src/
```
```bash
uvicorn src.app.main:app --reload
```
Либо используйте:
```bash
python main.py
```

Документация будет доступна по адресу: http://127.0.0.1:8000/docs
</details>

<details><summary><h2>Запуск проекта через докер</h2></summary>

1. Создайте .env файл с данными для подключения к бд:
```
POSTGRES_PASSWORD=password
```
2. Скопируйте файл docker-compose-prod.yaml в директорию с .env файлом.

3. Выполните команду:
```bash
docker compose -f .\docker-compose-prod.yaml up -d
```

Документация будет доступна по адресу: http://127.0.0.1:8000/docs
</details>

<details><summary><h2>Запуск проекта через докер без загрузки образа</h2></summary>

1. Клонируйте репозиторий, создайте виртуальное окружение и активируйте его.

2. Создайте .env файл с данными для подключения к бд:
```
POSTGRES_PASSWORD=password
```
3. Все настройки приложения находятся в файле src/config/config.yaml.

4. Запустите приложение из папки infra:
```bash
docker compose up -d
```
Документация будет доступна по адресу: http://127.0.0.1:8000/docs
</details>
<details><summary><h2>Запуск тестов</h2></summary>

1. Клонируйте репозиторий, создайте виртуальное окружение и активируйте его.

2. Установите poetry:
```bash
pip install poetry
```
3. Установите зависимости:
```bash
poetry install
```
4. Создайте .env файл с данными для подключения к бд:
```
POSTGRES_PASSWORD=password
```
5. Все настройки приложения находятся в файле src/config/config.yaml.
Так как тесты интеграционные необходима реальная бд.

6. Запустите тесты:
```bash
pytest --cov --cov-report term-missing
```
</details>

<details><summary><h2>Преимущества</h2></summary>

- реализовано в соответствии с заданием https://docs.google.com/document/d/12qJvn8WZAxDsFTOGBC2uiaAioIg4x3JF-TvGvq2Povs/edit?tab=t.0

- Там где это необходимо используется конкурентность.

- Покрытие тестами - 96%

- Реализовано CI/CD.

- Имеется дополнительный эндпоинт для отмены подписки.
</details>
