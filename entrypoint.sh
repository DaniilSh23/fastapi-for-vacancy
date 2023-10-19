#!/bin/bash

# Move to project directory
# shellcheck disable=SC2164
cd /fastapi_app

# Start server through gunicorn
echo "Starting server through uvicorn"
uvicorn main:APP --reload