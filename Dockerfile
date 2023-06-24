# -- Build step, in charge of compiling the frontend app
FROM node:20.2.0-bullseye-slim AS build

WORKDIR /app

COPY dnd5esheets/front/package.json ./
COPY dnd5esheets/front/package-lock.json ./
RUN npm install
COPY dnd5esheets/front/ ./
RUN npm run build


# -- Main build combining the FastAPI and compiled frontend apps
FROM python:3.11.4-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd5esheets ./dnd5esheets
COPY alembic.ini .
COPY scripts/start-app.sh .
RUN rm -r ./dnd5esheets/front/*
COPY --from=build /app/dist ./dnd5esheets/front/dist

CMD ./start-app.sh
