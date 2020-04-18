HASH := $(shell git rev-parse --short HEAD)
CONTAINER := uno/backend
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

build-image:
	docker build . -t $(CONTAINER):$(HASH)

push-keroku:
	git push heroku master
