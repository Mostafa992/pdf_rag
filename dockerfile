
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV CURRENT_TIME="2024-12-19T17:38:29+02:00"

CMD ["python", "app.py"]