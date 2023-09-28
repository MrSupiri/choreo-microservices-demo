FROM python:3-alpine

WORKDIR /app

COPY . /app

RUN pip install requests

USER 10014

CMD ["python", "main.py"]
