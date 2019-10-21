compile:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

run: compile \
	start
