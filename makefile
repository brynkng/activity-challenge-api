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
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

build-dev:
	docker-compose build