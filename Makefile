# Variables
PROJECT_NAME=todoapp
APICONTAINER := $(shell docker ps -q -f name="todo_app_be")
DBCONTAINER := $(shell docker ps -q -f name="todo_app_db")
COMPOSE=docker-compose
MANAGE=python manage.py

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
	$(MANAGE) makemigrations
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

lint:
	flake8 .

test:
	$(MANAGE) test

.PHONY: start stop restart logs shell dbshell migrations superuser lint test
