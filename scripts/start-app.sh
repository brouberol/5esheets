#!/bin/bash

set -e

alembic upgrade head
exec \
    env LD_PRELOAD=./lib/libsqlite3.so \
    uvicorn --factory dnd5esheets.app:create_app --host "0.0.0.0" --port 8000
