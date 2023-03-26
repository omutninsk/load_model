#!/bin/sh
set -e

case "$1" in
  start)
    python app.py
    ;;
  flower)
    celery -A celery worker
    ;;
  *)
    exec "$@"
esac