docker-compose down
docker-compose pull
docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
