# https://medium.com/thedevproject/setup-flask-project-using-docker-and-gunicorn-4dcaaa829620
# syntax=docker/dockerfile:1

FROM python:3.10.10-slim-buster

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]