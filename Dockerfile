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
    apt-get install -y build-essential wget tcl && \
    ./compile-libsqlite-linux.sh && \
    apt-get remove -y build-essential wget tcl && \
    apt clean


# -- Main build combining the FastAPI and compiled frontend apps
FROM python:3.11.4-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd5esheets ./dnd5esheets
COPY alembic.ini .
COPY scripts/start-app.sh .
RUN rm -r ./dnd5esheets/front/*
COPY --from=front-build /app/src/build/dist ./dnd5esheets/front/dist
COPY --from=sqlite-build /app/src/build/libsqlite3.so ./lib/libsqlite3.so

CMD ["./start-app.sh"]
