# Базовый образ Python
FROM python:3.9

RUN pip install --upgrade pip 

# Установка зависимостей
RUN apt-get update && apt-get install -y \
postgresql-client

# Установка переменной окружения для кодировки
ENV PYTHONIOENCODING=utf-8

# Создание директории приложения внутри контейнера
RUN mkdir /app
WORKDIR /app

# Копирование и установка зависимостей проекта
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копирование исходных файлов проекта внутрь контейнера
COPY . /app/

# Открытие порта для веб-сервера Django
EXPOSE 8000

# Запуск команды для миграции базы данных
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python manage.py tests lms.tests.benchmarks