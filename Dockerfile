FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update -yq && apt-get install -yqq python
RUN apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD wait-for-postgres.sh /code/
RUN chmod +x wait-for-postgres.sh

ADD . /code/

EXPOSE 8000

