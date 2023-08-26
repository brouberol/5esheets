# hadolint global ignore=DL3008
# -- Build step, in charge of compiling the frontend app
FROM node:20.2.0-bullseye-slim AS front-build

WORKDIR /app/src/build

COPY dnd5esheets/front/package.json ./
COPY dnd5esheets/front/package-lock.json ./
RUN npm install
COPY dnd5esheets/front/ ./
RUN npm run build


# -- Build the libsqlite3.so shared object for the appropriate architecture
FROM python:3.11.4-slim AS sqlite-build

WORKDIR /app/src/build

COPY scripts/compile-libsqlite-linux.sh ./
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential wget tcl && \
    ./compile-libsqlite-linux.sh && \
    apt-get remove -y build-essential wget tcl && \
    apt-get auto-clean


# -- Generate the requirements.txt file
FROM python:3.11.4-slim AS reqstxt-build

WORKDIR /app/src/build
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install --no-cache-dir poetry==1.6.1 && poetry export --without=dev -o requirements.txt


# -- Main build combining the FastAPI and compiled frontend apps
FROM python:3.11.4-slim

ARG USERNAME=app
ARG USER_UID=1000
ARG USER_GID=$USER_UID
WORKDIR /usr/src/app

RUN addgroup --gid $USER_GID app && \
    adduser --uid $USER_UID --gid $USER_GID --disabled-password $USERNAME
COPY --from=reqstxt-build /app/src/build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd5esheets ./dnd5esheets
COPY alembic.ini .
COPY scripts/start-app.sh .
RUN rm -r ./dnd5esheets/front/*
COPY --from=front-build /app/src/build/dist ./dnd5esheets/front/dist
COPY --from=sqlite-build /app/src/build/libsqlite3.so ./lib/libsqlite3.so
USER $USERNAME
CMD ["./start-app.sh"]
