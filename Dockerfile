FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["dagster", "dev", "-m", "dagster_project.definitions", "-h", "0.0.0.0", "-p", "3000"]