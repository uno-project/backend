
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
