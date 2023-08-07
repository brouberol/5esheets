#!/bin/bash

set -e

alembic upgrade head
exec uvicorn --factory dnd5esheets.app:create_app --host "0.0.0.0" --port 8000 --no-access-log
