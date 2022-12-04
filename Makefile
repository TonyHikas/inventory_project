PROJECT_NAME?=inventory_project
export COMPOSE_PROJECT_NAME?=$(PROJECT_NAME)

COMPOSE_CMD=docker-compose -p $(COMPOSE_PROJECT_NAME)

shell:
	$(COMPOSE_CMD) exec app /bin/bash -c python

exec:
	$(COMPOSE_CMD) exec app /bin/bash

build:
	$(COMPOSE_CMD) build

run:
	$(COMPOSE_CMD) up

logs:
	$(COMPOSE_CMD) logs -f app

poetry:
	$(COMPOSE_CMD) "cd /app && poetry $(call args)"

make_migrations:
	$(COMPOSE_CMD) "alembic revision --autogenerate -m $(call args)"

migrate:
	$(COMPOSE_CMD) "alembic upgrade head"


