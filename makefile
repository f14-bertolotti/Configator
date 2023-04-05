

.PHONY: test

test:
	python3 -m unittest tests/Configator.py
	python3 -m unittest tests/Fielder.py
