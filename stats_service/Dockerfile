FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50052

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-u", "stats_service_app/main.py"]