#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
# exec gunicorn activityChallengeApi.wsgi:application \
#     --bind 0.0.0.0:$PORT \
#     --workers 3


#!/bin/bash

function manage_app () {
    python manage.py makemigrations
    python manage.py migrate
}

function start_development() {
    # use django runserver as development server here.
    manage_app
    npm run dev

    while true; do
        echo "Restarting django run server!"
        python manage.py runserver_plus 0.0.0.0:5000
        sleep 2
    done
}

function start_production() {
    # use gunicorn for production server here
    manage_app
    npm run build

    python manage.py collectstatic --noinput
    
    gunicorn activityChallengeApi.wsgi:application -w 4 -b 0.0.0.0:$PORT --chdir=/app
}

if [ ${PRODUCTION} == "true" ]; then
    # use production server
    echo "Using production server"
    start_production
else
    # use development server
    echo "Using development server"
    start_development
fi