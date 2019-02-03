start-dev:
	docker-compose up

start-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

shell:
	docker exec -it django_web python manage.py shell_plus

stop-compose:
	@eval docker stop $$(docker ps -a -q)
	docker-compose down

ssh-django-web:
	docker exec -it django_web bash

ssh-db:
	docker exec -it db bash

check-network-config-details:
	docker network inspect activitychallengeapi_default

build-prod:
	# docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

build-dev:
	docker-compose build

activity_challenge_api_django_web:1.0

prod-shell:
	heroku run python manage.py shell

deploy:
	npm run build && \
	make build-prod && \
	docker tag activity_challenge_api_django_web:1.0 registry.heroku.com/activity-challenge-api/web && \
	docker push registry.heroku.com/activity-challenge-api/web:latest && \
	heroku container:release web