#!/bin/bash

alembic upgrade head
exec uvicorn dnd5esheets.app:app --host "0.0.0.0" --port 8000
