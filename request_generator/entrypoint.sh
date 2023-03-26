#!/bin/sh
set -e

case "$1" in
  start)
    python app.py
    ;;
  tasks)
    celery -A app.celery worker -l INFO -n Worker
    ;;
  flower)
    celery -A app.celery flower -l INFO
    ;;
  *)
    exec "$@"
esac