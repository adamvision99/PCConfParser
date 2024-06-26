# PCConfParser

PCConfParser — это бот на Python, разработанный для автоматизации процесса извлечения данных о товарах из нескольких интернет-магазинов, что способствует оптимизации бизнес-процессов и повышению оперативности предприятия. Данный проект сосредоточен на разработке, тестировании и внедрении веб-скрейпинг бота с использованием Scrapy и сопутствующих инструментов.

## Обзор проекта

### Цель
Основной целью данного проекта является повышение эффективности обработки заказов путем разработки и тестирования веб-скрейпинг бота. Бот, созданный на языке Python, предназначен для автоматизации процесса обработки данных о товарах, поступающих из различных интернет-магазинов, что способствует оптимизации бизнес-процессов и повышению оперативности компании.

### Особенности
- **Извлечение данных**: Автоматический сбор данных о товарах из различных интернет-магазинов.
- **Обход защит**: Использование инструментов для обхода защит от ботов, таких как Cloudflare.
- **Интеграция с Google Sheets**: Автоматическое занесение собранных данных в Google Sheets для удобства хранения и обработки.

## Установка и настройка

### Требования
- Python 3.6 и выше
- Scrapy
- Scrapyd
- ScrapydWeb
- FlareSolverr
- Google Sheets API

### Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/adamvision99/PCConfParser
    cd PCConfParser
    ```

2. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Настройте Google Sheets API:
    - Создайте учетную запись в Google Cloud Platform.
    - Создайте сервисный аккаунт и скачайте файл ключа JSON.
    - Сохраните файл ключа JSON в корневую директорию проекта и назовите его `client_key.json`.

4. Настройте переменные окружения:
    ```bash
    export GOOGLE_CLOUD_KEYFILE_JSON=client_key.json
    ```

## Использование

1. Запустите Scrapyd для управления задачами скрейпинга:
    ```bash
    scrapyd
    ```

2. Запустите ScrapydWeb для мониторинга выполнения задач:
    ```bash
    scrapydweb
    ```

3. Загрузите проект на Scrapyd:
    ```bash
    curl http://localhost:6800/addversion.json -F project=pcconfparser -F version=r1.0 -F egg=@dist/pcconfparser-1.0-py3.6.egg
    ```

4. Запустите задания скрейпинга:
    ```bash
    curl http://localhost:6800/schedule.json -d project=pcconfparser -d spider=<spider_name>
    ```

## Спасибо за внимание

Мы приветствуем вклад в развитие проекта. Пожалуйста, создавайте пул-реквесты и открывайте задачи для предложений и багов.

