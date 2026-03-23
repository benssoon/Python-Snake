ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

WORKDIR /app
COPY python_snake.py .

RUN chmod +x ./python_snake.py

CMD ["python3", "python_snake.py" ]