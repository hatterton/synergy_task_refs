APP_NAME = synergy_refs

.PHONY: run
run:
	docker-compose up $(APP_NAME)

.PHONY: migrate
migrate:
	docker-compose run $(APP_NAME) python manage.py makemigrations refs
	docker-compose run $(APP_NAME) python manage.py migrate

.PHONY: reload-data
reload-data:
	docker-compose run $(APP_NAME) python manage.py flush --no-input
	docker-compose run $(APP_NAME) python manage.py shell -c "from refs.utils import load_user_graph_data; load_user_graph_data()"

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
