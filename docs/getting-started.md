This project is intended to be run on Linux or macOS, and requires [`poetry`](https://python-poetry.org/docs/#installing-with-the-official-installer) and [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) to be installed to install python and javascript dependencies.

We however provide a [docker](https://docs.docker.com/desktop/) image to run the application if somehow installing these tools prove troublesome.

## Running the project in docker

To run both the backend API and the frontend app in docker, you simply have to run

```bash
make dev
```

This will:

- build the docker image for the backend app, with all dependencies installed
- build the docker image for the frontend app, with all dependencies installed
- run both images via docker compose
- apply the SQL migrations
- populate the database with items, spells and development fixtures

## Running the project without containers

If you were confortable installing `poetry` and `npm` on your development machine, and managed to, then run

```bash
make init
```

This will:

- install all backend dependencies
- install all frontend dependencies
- apply the SQL migrations
- populate the database with items, spells and development fixtures

At that point, open 2 terminal tabs. Run the following command in the first tab to run the backend application:

```bash
make run
```

Run this command in the second terminal tab to run the frontend application:

```bash
make run-front-dev
```

## Next steps

At that point, the backend API will run under `http://localhost:8000` and the frontend will run under `http://localhost:3000`

!!! note

    Any edit you make in the codebase while running `make dev` will induce automatic reload of either the backend or frontend application.
