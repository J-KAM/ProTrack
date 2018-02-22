docker-compose down
docker-compose pull
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up -d