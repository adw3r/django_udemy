docker-compose build app
docker-compose kill app
docker-compose kill nginx
docker-compose up app -d
docker-compose up nginx -d
