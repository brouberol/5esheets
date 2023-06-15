.DEFAULT_GOAL = help
.PHONY: dev docker-build docker-run run help

5esheets/translations/messages.pot: 5esheets/templates/*.html
	poetry run pybabel extract --omit-header -F babel.cfg -o 5esheets/translations/messages.pot .

$(wildcard 5esheets/translations/*/*/messages.po): 5esheets/translations/messages.pot
	poetry run pybabel update --omit-header --no-fuzzy-matching -i 5esheets/translations/messages.pot -d 5esheets/translations

$(wildcard 5esheets/translations/*/*/messages.mo): $(wildcard 5esheets/translations/*/*/messages.po)
	poetry run pybabel compile --use-fuzzy -d 5esheets/translations

run:  ## Run the server
	cd 5esheets && poetry run flask run --port 8000 --reload --debug

translations-extract: 5esheets/translations/messages.pot  ## Extract all strings to translate from jinja templates

translations-update: $(wildcard 5esheets/translations/*/*/messages.po)  ## Update the language catalogs with new translations

translations-compile: $(wildcard 5esheets/translations/*/*/messages.mo)  ## Compile translations into a .mo file

dev:  ## Install the development environment
	poetry install

docker-build:  $(wildcard 5esheets/translations/*/*/messages.mo)  ## Build the docker image
	docker build -t brouberol/5esheets .

docker-run:  docker-build ## Run the docker image
	docker run -it --rm -v $$(pwd)/5esheets/db:/usr/src/app/db/ -p 8000:8000 brouberol/5esheets

migratedb:  ## Run the SQL migrations
	poetry run caribou upgrade 5esheets/db/5esheets.db 5esheets/migrations

help:  ## Display help
	@grep -E '^[%a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'
