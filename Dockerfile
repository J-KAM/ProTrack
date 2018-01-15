FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


