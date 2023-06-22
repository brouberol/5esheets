.DEFAULT_GOAL = help
.PHONY: dnd5esheets/templates/spellbook.html dev docker-build docker-run run help

dnd5esheets/translations/messages.pot: dnd5esheets/templates/*.html
	poetry run pybabel extract --omit-header -F babel.cfg -o dnd5esheets/translations/messages.pot .

$(wildcard dnd5esheets/translations/*/*/messages.po): dnd5esheets/translations/messages.pot
	poetry run pybabel update --omit-header --no-fuzzy-matching -i dnd5esheets/translations/messages.pot -d dnd5esheets/translations

$(wildcard dnd5esheets/translations/*/*/messages.mo): $(wildcard dnd5esheets/translations/*/*/messages.po)
	poetry run pybabel compile --use-fuzzy -d dnd5esheets/translations

dnd5esheets/templates/spellbook.html:
	python3 scripts/generate_spellbook.py > dnd5esheets/templates/spellbook.html

api-doc:  ## Open the 5esheets API documentation
	open http://localhost:8000/redoc

dev:  ## Install the development environment
	poetry install

docker-build:  ## Build the docker image
	docker build -t brouberol/5esheets .

docker-run:  docker-build  ## Run the docker image
	docker run -it --rm -v $$(pwd)/dnd5esheets/db:/usr/src/app/dnd5esheets/db/ -p 8000:8000 brouberol/5esheets

db-migrate:  ## Run the SQL migrations
	poetry run alembic upgrade head

db-dev-fixtures:  ## Populate the local database with development fixtures
	poetry run python3 dnd5esheets/cli.py db populate

translations-extract: dnd5esheets/translations/messages.pot  ## Extract all strings to translate from jinja templates

translations-update: $(wildcard dnd5esheets/translations/*/*/messages.po)  ## Update the language catalogs with new translations

translations-compile: $(wildcard dnd5esheets/translations/*/*/messages.mo)  ## Compile translations into a .mo file

run:  ## Run the server
	cd dnd5esheets && poetry run flask run --port 8000 --reload --debug

help:  ## Display help
	@grep -E '^[%a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'
