# -- Build step, in charge of compiling the Svelte app
FROM node:20.2.0-bullseye-slim AS build

WORKDIR /app

COPY dnd5esheets/client/package.json ./
COPY dnd5esheets/client/package-lock.json ./
RUN npm install
COPY dnd5esheets/client/ ./
RUN npm run build


# -- Main build combining the FastAPI and compiled Svelte apps
FROM python:3.11.4-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnd5esheets ./dnd5esheets
COPY --from=build /app/dist ./dnd5esheets/client/dist

CMD ["uvicorn", "dnd5esheets.app:app", "--host", "0.0.0.0", "--port", "8000"]
