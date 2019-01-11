# EloLeft4Dead2-AKA-Spil


### What the heck is that ?

Well, if you don't know why your are here, please go away...

Deal with it

### Introduction
This project provides a docker container with :

- Python 3.6
- Nginx
- MongoDB
- uWsgi
- supervisor
- Flask python microframework (API)
- some useful python packages such as numpy, scipy... (add more in requirements.txt) for duche mainly... or whothefuck read this 
- Nosetests

### Installation

- Clone project :
```
cd /code/app/
git clone https://github.com/laurentmorelli/EloLeft4Dead2-AKA-Spil
cd EloLeft4Dead2-AKA-Spil
```
- Build docker image :
```
docker build -t spil_prod_image -f ./docker/prod-image/Dockerfile .
docker build -t spil_test_image -f ./docker/test-image/Dockerfile .
```
- Start container :
```
docker-compose -f docker-compose.dev.yml up -d
```
- You can now access [web front-end](http://localhost:8084/front/index.html) and start using endpoints.

If you need to go inside container : `docker-compose -f docker-compose.dev.yml exec spil bash`

To restart dev docker :
```
docker stop spil && docker-compose -f docker-compose.dev.yml up -d && docker exec -it spil bash
```

### Run unit tests

```
docker exec spil nosetests
```

### Brutal clean of all dockers

```
docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls | tail -n+2 | awk '{if($2 !~ /bridge|none|host/){ print $1 }}')
```

### clean pyc

```
find . -name "*.pyc" -exec rm -f {} \;
```
