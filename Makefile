
default: test

test:
	python3 -m pytest

lint:
	yapf -i -r uno
	yapf -i -r tests
