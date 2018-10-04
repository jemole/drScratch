SRC?=$(shell dirname `pwd`)

build:
	docker-compose build
up:
	docker-compose up
migrate:
	docker-compose run web python manage.py migrate


