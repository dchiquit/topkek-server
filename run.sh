#!/bin/sh

source venv/bin/activate
export FLASK_APP=topkek
export FLASK_ENV=development
export FLASK_RUN_PORT=5001
flask run