APP_NAME = synergy_refs

# Containers
.PHONY: run
run:
	docker-compose up $(APP_NAME)

.PHONY: build
build:
	docker-compose build

.PHONY: shell
shell:
	docker-compose run $(APP_NAME) bash

.PHONY: attach
attach:
	docker-compose exec -ti $(APP_NAME) bash


.PHONY: tests
tests: tests
	docker-compose run $(APP_NAME) pytest refs/tests.py
	@echo "All tests passed"


.PHONY: run-local
run-local:
	cd src && poetry run python synergy_refs/manage.py runserver


.PHONY: poetry-shell
poetry-shell:
	cd src && poetry shell
