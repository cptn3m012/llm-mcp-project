FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary
COPY server.py .
EXPOSE 3330
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3330"]