FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update -yq && apt-get install -yqq python
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


