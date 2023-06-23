.DEFAULT_GOAL = help
.PHONY: api-doc api-explorer black check dev dnd5esheets/templates/spellbook.html \
	docker-build docker-run init mypy ruff run svelte-check svelte-build \
	svelte-generate-api-client help

dnd5esheets/translations/messages.pot: dnd5esheets/templates/*.html
	poetry run pybabel extract --omit-header -F babel.cfg -o dnd5esheets/translations/messages.pot .

$(wildcard dnd5esheets/translations/*/*/messages.po): dnd5esheets/translations/messages.pot
	poetry run pybabel update --omit-header --no-fuzzy-matching -i dnd5esheets/translations/messages.pot -d dnd5esheets/translations

$(wildcard dnd5esheets/translations/*/*/messages.mo): $(wildcard dnd5esheets/translations/*/*/messages.po)
	poetry run pybabel compile --use-fuzzy -d dnd5esheets/translations

dnd5esheets/templates/spellbook.html:
	python3 scripts/generate_spellbook.py > dnd5esheets/templates/spellbook.html

dnd5esheets/client/openapi.json:
	curl http://localhost:8000/openapi.json | python3 -m json.tool > dnd5esheets/client/openapi.json

dnd5esheets/schemas.py:

api-doc:  ## Open the 5esheets API documentation
	open http://localhost:8000/redoc

api-explorer:  ## Open the 5esheets API explorer (allowing request executiojs)
	open http://localhost:8000/docs

build: svelte-build  ## Build the application

black:
	poetry run black dnd5esheets/

check: black mypy ruff svelte-check ## Run all checks on the python codebase

dev:  ## Install the development environment
	poetry install
	cd dnd5esheets/client && npm install

docker-build:  build requirements.txt  ## Build the docker image
	docker build -t brouberol/5esheets .

docker-run:  docker-build  ## Run the docker image
	docker run -it --rm -v $$(pwd)/dnd5esheets/db:/usr/src/app/dnd5esheets/db/ -p 8000:8000 brouberol/5esheets

db-migrate:  ## Run the SQL migrations
	poetry run alembic upgrade head

db-dev-fixtures:  db-migrate ## Populate the local database with development fixtures
	poetry run python3 dnd5esheets/cli.py db populate

init:  dev db-dev-fixtures run  ## Run the application for the first time

mypy:
	poetry run mypy dnd5esheets/

poetry.lock: pyproject.toml
	poetry lock

pyproject.toml:

requirements.txt: poetry.lock
	poetry export --without=dev -o requirements.txt

svelte-build:
	cd dnd5esheets/client && npm run build

svelte-check:
	cd dnd5esheets/client && npm run check

svelte-generate-api-client: dnd5esheets/client/openapi.json  ## Generate the typescript client for the 5esheet API
	cd dnd5esheets/client && npm run generate-client

ruff:
	poetry run ruff --fix dnd5esheets/

run: build  ## Run the app
	cd dnd5esheets && poetry run uvicorn dnd5esheets.app:app --reload

translations-extract: dnd5esheets/translations/messages.pot  ## Extract all strings to translate from jinja templates

translations-update: $(wildcard dnd5esheets/translations/*/*/messages.po)  ## Update the language catalogs with new translations

translations-compile: $(wildcard dnd5esheets/translations/*/*/messages.mo)  ## Compile translations into a .mo file



help:  ## Display help
	@grep -E '^[%a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}'
