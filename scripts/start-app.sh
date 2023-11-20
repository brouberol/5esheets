#!/bin/bash

set -e
alembic upgrade head
if [ ${DND5ESHEETS_ENV} = "dev" ]; then
    PYTHONPATH=. python3 dnd5esheets/cli.py db populate all
fi
exec \
    env LD_PRELOAD=./lib/libsqlite3.so \
    uvicorn --factory dnd5esheets.app:create_app --host "0.0.0.0" --port 8000 --reload
