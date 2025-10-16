FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY retrieval ./retrieval
COPY metrics ./metrics
COPY service ./service
COPY evaluation ./evaluation

EXPOSE 8000
CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", 8000]
