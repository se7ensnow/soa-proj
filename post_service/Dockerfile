FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "-u", "post_service_app/main.py"]