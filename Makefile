HASH := $(shell git rev-parse --short HEAD)
CONTAINER := uno/backend
SERVICE_NAME=uno

default: test

test-unittest:
	python3 -m pytest tests/unittest

test-rest:
	python3 -m pytest tests/rest

lint:
	yapf -i -r uno
	yapf -i -r tests

clean:
	rm coverage.xml
	rm -rf build htmlcov
	find . -name __pycache__ | xargs rm -rf

api:
	gunicorn --bind 0.0.0.0:8080 'rest:create_app()'

build-image:
	docker build . -t $(CONTAINER):$(HASH)

push-keroku:
	git push heroku master
