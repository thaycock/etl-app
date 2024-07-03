#!/bin/bash

poetry config virtualenvs.create false
poetry install
export FLASK_APP=apihealth.src.health.api:app
export FLASK_ENV=development
export FLASK_DEBUG=1
echo $FLASK_APP
flask run --debugger -h 0.0.0.0 -p 5000 --reload
