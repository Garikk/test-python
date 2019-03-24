#!/usr/bin/env sh

echo "Waiting for DB"

until python docker/check_pq.py;
do
  echo "  ..."
  sleep 1
done
echo "  UP!"

flask db upgrade

if [ $FLASK_ENV == "development" ]; then
  echo "Running DEV server"
  FLASK_DEBUG=1 flask run --host 0.0.0.0 --port $GUNICORN_PORT
else
  echo "Running PROD server"
  FLASK_ENV=$FLASK_ENV gunicorn --bind 0.0.0.0:$GUNICORN_PORT $GUNICORN_MODULE:$GUNICORN_CALLABLE
fi
