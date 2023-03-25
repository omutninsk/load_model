#!/bin/sh
set -e

case "$1" in
  start)
    python app.py
    ;;
  app1)
    python app.py
    ;;
  app2)
    python app.py
    ;;
  *)
    exec "$@"
esac