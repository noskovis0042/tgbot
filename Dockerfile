# Используем официальный образ Python
FROM python:3.13-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем все библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Команда запуска
CMD ["python", "bot.py"]