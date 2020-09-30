web: daphne AINOTE.asgi:application --port $PORT --bind 0.0.0.0
worker: gunicorn --pythonpath AINOTE AINOTE.wsgi --log-file -