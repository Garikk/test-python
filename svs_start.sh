#!/bin/sh

#export FLASK_ENV=development

if [ "$1" = "db" ]; then
    flask db $2
    exit
fi

if [ "$1" = "test" ]; then
    pytest
    exit
fi
flask run
