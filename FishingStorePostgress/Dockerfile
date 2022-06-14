FROM python:3.9-slim-buster

RUN apt-get update; \
	apt-get install -y --no-install-recommends;

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip3 install --upgrade pip; \
    pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app
CMD gunicorn mysite.wsgi
EXPOSE 8000