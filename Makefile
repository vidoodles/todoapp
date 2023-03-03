# Variables
PROJECT_NAME=todoapp
APICONTAINER := $(shell docker ps -q -f name="todo_app_be")
DBCONTAINER := $(shell docker ps -q -f name="todo_app_db")
COMPOSE=docker-compose
MANAGE=docker c

# Commands
start:
	$(COMPOSE) up -d

stop:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d --build

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec web bash

dbshell:
	$(COMPOSE) exec db psql -U postgres -d todolist_db

migrations:
	$(COMPOSE) exec web python manage.py makemigrations
	$(COMPOSE) exec web python manage.py migrate

superuser:
	$(COMPOSE) run web python manage.py createsuperuser

lint:
	flake8 .

test:
	$(COMPOSE) exec web python manage.py test

.PHONY: start stop restart logs shell dbshell migrations superuser lint test
