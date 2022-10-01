HASH := $(shell git rev-parse --short HEAD)
CONTAINER := eu.gcr.io/uno-project-364221/backend
SERVICE_NAME=uno

default: test

test:
	python3 -m pytest

lint:
	yapf -i -r uno
	yapf -i -r tests

clean:
	rm coverage.xml
	rm -rf build htmlcov
	find . -name __pycache__ | xargs rm -rf

api:
	gunicorn --bind 0.0.0.0:8080 'rest:create_app()' --access-logfile '-' --error-logfile '-' --worker-class gevent

build-image:
	docker build . -t $(CONTAINER):$(HASH)

docker-push:
	docker tag $(CONTAINER):$(HASH) $(CONTAINER):latest
	docker push $(CONTAINER):latest

