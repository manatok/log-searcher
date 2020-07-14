run:
	@echo "Starting up the environment in Docker"
	docker-compose up --build

run_background:
	@echo "Starting up the application in the background"
	docker-compose up -d --build

stop:
	@stopping the application
	docker-compose down

test:
	python -m unittest

test_smoke: run_background
	./app/test/smoke/env_ready.sh
	@echo "API ready, running tests"
	python -m unittest app/test/smoke/logging.py
	docker-compose down

	