FROM python:3.10-slim

WORKDIR /app

COPY server/ ./server/
COPY docs/ ./docs/
COPY server/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"] 