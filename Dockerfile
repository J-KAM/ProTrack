FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update -yq && apt-get install -yqq python
RUN apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN mkdir /code
ADD requirements.txt /code/
RUN pip install -r /code/requirements.txt


ADD . /code/
WORKDIR /code


EXPOSE 8000
CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0 8000

