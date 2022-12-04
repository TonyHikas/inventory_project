PROJECT_NAME?=inventory_project
export COMPOSE_PROJECT_NAME?=$(PROJECT_NAME)

COMPOSE_CMD=docker-compose -p $(COMPOSE_PROJECT_NAME)
COMPOSE_ONCE=$(COMPOSE_CMD) run --rm app /bin/bash -c

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

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${args:-$arg:-${1}}}`

poetry:
	$(COMPOSE_ONCE) "cd /app && poetry $(call args)"

makemigrations:
	$(COMPOSE_ONCE) "poetry run alembic revision --autogenerate -m $(call args)"

migrate:
	$(COMPOSE_ONCE) "poetry run alembic upgrade head"

%:
	@:


