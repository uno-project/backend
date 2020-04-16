HASH := $(shell git rev-parse --short HEAD)
CONTAINER := gcr.io/booming-cairn-261420/app
default: test
SERVICE_NAME=uno

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

push-image:
	docker tag $(CONTAINER):$(HASH) $(CONTAINER):latest
	docker push $(CONTAINER):latest
	gcloud run deploy $(SERVICE_NAME) --image $(CONTAINER):latest --region us-central1 --platform 'managed' --allow-unauthenticated
